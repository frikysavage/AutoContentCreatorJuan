import pytest
from fastapi.testclient import TestClient
from services.video_service.main import app
from unittest.mock import patch

client = TestClient(app)

@patch('services.video_service.main.get_provider')
def test_generate_visuals(mock_get_provider):
    mock_provider = mock_get_provider.return_value
    mock_provider.generate_clips.return_value = ["http://mock-url.com/clip1.mp4"]
    
    response = client.post("/generate-visuals", json={
        "guion": "Hola a todos",
        "personajes": [],
        "ficha_personaje": {},
        "formato": "shorts"
    })
    
    assert response.status_code == 200
    assert response.json()["clips"] == ["http://mock-url.com/clip1.mp4"]
