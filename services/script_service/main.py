import json
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import desc

from shared.db.database import get_db
from shared.db.models import Account, CharacterSheet, VideoHistory
from services.script_service.llm_client import generate_script_llm

app = FastAPI(title="Script Service")

class ScriptRequest(BaseModel):
    account_id: int
    tema: str
    duracion_segundos: int = None
    formato: str = None
    musica: str = "Cualquier estilo"
    subtitulos: bool = True

@app.post("/generate-script")
def generate_script(req: ScriptRequest, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == req.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Fallback to account defaults if not provided
    duracion = req.duracion_segundos or account.duracion_default or 60
    formato = req.formato or account.formato_default or "shorts"
    subtitulos_str = "Sí" if req.subtitulos else "No"
    
    # Get active character sheet
    sheet = db.query(CharacterSheet).filter(CharacterSheet.account_id == req.account_id).order_by(desc(CharacterSheet.creado_en)).first()
    ficha_previa = "Ninguna"
    if sheet:
        ficha_previa = json.dumps({
            "estilo": sheet.estilo,
            "rasgos_fijos": sheet.rasgos_fijos,
            "paleta": sheet.paleta,
            "vestuario_base": sheet.vestuario_base
        })

    # Get last 5 videos for anti-repetition
    history = db.query(VideoHistory).filter(VideoHistory.account_id == req.account_id).order_by(desc(VideoHistory.creado_en)).limit(5).all()
    historial_str = "\n".join([f"- {h.resumen_para_historial}" for h in history]) if history else "Ninguno"

    # Call LLM
    try:
        resultado = generate_script_llm(
            tema=req.tema,
            cuenta=account.nombre,
            categoria=account.categoria_default,
            idioma=account.idioma_default,
            duracion_segundos=duracion,
            formato=formato,
            con_o_sin_subtitulos=subtitulos_str,
            musica=req.musica,
            ficha_personaje_previa=ficha_previa,
            historial_guiones=historial_str
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Parse and save new character sheet if applicable
    ficha_resultado = resultado.get("ficha_personaje", {})
    if ficha_resultado.get("nueva_o_reutilizada") == "nueva":
        new_sheet = CharacterSheet(
            account_id=req.account_id,
            estilo=ficha_resultado.get("estilo"),
            rasgos_fijos=ficha_resultado.get("rasgos_fijos"),
            paleta=ficha_resultado.get("paleta"),
            vestuario_base=ficha_resultado.get("vestuario_base")
        )
        db.add(new_sheet)
    
    # Save to history
    resumen = resultado.get("resumen_para_historial", "Generado sin resumen")
    new_history = VideoHistory(
        account_id=req.account_id,
        resumen_para_historial=resumen
    )
    db.add(new_history)
    
    db.commit()

    return resultado
