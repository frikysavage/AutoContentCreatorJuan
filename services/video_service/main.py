from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

from shared.config.settings import settings
from services.video_service.providers.vidu import ViduProvider

app = FastAPI(title="Video Service")

class VisualsRequest(BaseModel):
    guion: str
    personajes: List[Dict] = []
    ficha_personaje: Dict = {}
    formato: str = "shorts"

def get_provider():
    provider_name = settings.VIDEO_PROVIDER.lower()
    if provider_name == "vidu":
        return ViduProvider()
    else:
        # Fallback or other providers
        return ViduProvider()

@app.post("/generate-visuals")
def generate_visuals(req: VisualsRequest):
    try:
        provider = get_provider()
        clips = provider.generate_clips(
            guion=req.guion,
            personajes=req.personajes,
            ficha_personaje=req.ficha_personaje,
            formato=req.formato
        )
        return {"clips": clips}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
