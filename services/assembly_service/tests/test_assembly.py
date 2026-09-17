import pytest
from fastapi.testclient import TestClient
from services.assembly_service.main import app
from unittest.mock import patch

client = TestClient(app)

@patch('services.assembly_service.main.generate_tts_and_srt')
@patch('services.assembly_service.main.assemble_video')
def test_assemble(mock_assemble, mock_tts):
    mock_tts.return_value = ("/tmp/audio.mp3", "/tmp/subs.srt")
    mock_assemble.return_value = "/tmp/final.mp4"
    
    response = client.post("/assemble", json={
        "clips": ["clip1.mp4"],
        "guion": "Hola",
        "subtitulos": True,
        "musica": "rock",
        "idioma": "es",
        "formato": "shorts"
    })
    
    assert response.status_code == 200
    assert response.json()["video_path"] == "/tmp/final.mp4"
