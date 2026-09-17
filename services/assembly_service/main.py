import os
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from services.assembly_service.tts_client import generate_tts_and_srt
from services.assembly_service.ffmpeg_processor import assemble_video

app = FastAPI(title="Assembly Service")

class AssemblyRequest(BaseModel):
    clips: List[str]
    guion: str
    subtitulos: bool
    musica: str
    idioma: str
    formato: str = "shorts"

@app.post("/assemble")
def assemble(req: AssemblyRequest):
    try:
        # 1. Generate TTS and SRT
        audio_path, srt_path = generate_tts_and_srt(
            guion=req.guion,
            idioma=req.idioma,
            subtitulos=req.subtitulos
        )
        
        # 2. Assemble everything with FFmpeg
        # Output to a shared volume or cloud storage in reality
        output_filename = f"/tmp/final_video_{uuid.uuid4().hex}.mp4"
        final_video_path = assemble_video(
            clips_paths=req.clips,
            audio_path=audio_path,
            srt_path=srt_path,
            output_path=output_filename,
            formato=req.formato,
            musica=req.musica
        )
        
        return {"video_path": final_video_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
