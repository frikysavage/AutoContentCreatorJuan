import uuid
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from shared.db.database import get_db
from shared.db.models import VideoJob
from shared.config.settings import settings
from services.publish_service.youtube_client import upload_to_youtube, set_video_public

app = FastAPI(title="Publish Service")

class UploadRequest(BaseModel):
    video_path: str
    account_id: int
    titulo_seo: str
    descripcion: str
    synthetic_content: bool

@app.post("/upload-for-review")
def upload_for_review(req: UploadRequest, db: Session = Depends(get_db)):
    try:
        # Upload as unlisted
        video_id = upload_to_youtube(
            video_path=req.video_path,
            titulo=req.titulo_seo,
            descripcion=req.descripcion,
            synthetic_content=req.synthetic_content
        )
        
        # Generate review token
        review_token = uuid.uuid4().hex
        
        # Update or create VideoJob
        job = db.query(VideoJob).filter(VideoJob.account_id == req.account_id).order_by(VideoJob.creado_en.desc()).first()
        if not job:
            job = VideoJob(account_id=req.account_id)
            db.add(job)
            
        job.video_id_youtube = video_id
        job.review_token = review_token
        job.estado = "esperando_revision"
        db.commit()
        
        unlisted_url = f"https://youtu.be/{video_id}"
        
        return {
            "video_id": video_id,
            "review_token": review_token,
            "unlisted_url": unlisted_url,
            "confirm_url": f"{settings.PUBLIC_BASE_URL}/confirm/{review_token}",
            "reject_url": f"{settings.PUBLIC_BASE_URL}/reject/{review_token}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/confirm/{review_token}", response_class=HTMLResponse)
def confirm_video(review_token: str, db: Session = Depends(get_db)):
    job = db.query(VideoJob).filter(VideoJob.review_token == review_token).first()
    if not job:
        return HTMLResponse("<h1>Enlace inválido o expirado.</h1>", status_code=404)
        
    if job.estado != "esperando_revision":
        return HTMLResponse(f"<h1>El video ya fue procesado. Estado actual: {job.estado}</h1>", status_code=400)
        
    try:
        set_video_public(job.video_id_youtube)
        job.estado = "publicado"
        db.commit()
        return HTMLResponse("<h1>¡Video publicado con éxito!</h1>")
    except Exception as e:
        return HTMLResponse(f"<h1>Error al publicar: {str(e)}</h1>", status_code=500)

@app.get("/reject/{review_token}", response_class=HTMLResponse)
def reject_video(review_token: str, db: Session = Depends(get_db)):
    job = db.query(VideoJob).filter(VideoJob.review_token == review_token).first()
    if not job:
        return HTMLResponse("<h1>Enlace inválido o expirado.</h1>", status_code=404)
        
    if job.estado != "esperando_revision":
        return HTMLResponse(f"<h1>El video ya fue procesado. Estado actual: {job.estado}</h1>", status_code=400)
        
    job.estado = "rechazado"
    db.commit()
    return HTMLResponse("<h1>Video rechazado. Permanecerá como 'No listado' en YouTube.</h1>")
