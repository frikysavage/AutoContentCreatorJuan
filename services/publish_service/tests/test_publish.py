import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from services.publish_service.main import app

client = TestClient(app)

@patch('services.publish_service.main.upload_to_youtube')
def test_upload_for_review(mock_upload):
    mock_upload.return_value = "youtube123"
    
    mock_db = MagicMock()
    mock_db.query().filter().order_by().first.return_value = None
    
    from services.publish_service.main import get_db
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.post("/upload-for-review", json={
        "video_path": "/tmp/vid.mp4",
        "account_id": 1,
        "titulo_seo": "test",
        "descripcion": "desc",
        "synthetic_content": True
    })
    
    assert response.status_code == 200
    assert response.json()["video_id"] == "youtube123"
    assert "review_token" in response.json()
