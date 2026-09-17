import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from services.script_service.main import app

client = TestClient(app)

@patch('services.script_service.main.get_db')
@patch('services.script_service.main.generate_script_llm')
def test_generate_script(mock_llm, mock_get_db):
    mock_db = MagicMock()
    mock_account = MagicMock()
    mock_account.nombre = "test account"
    mock_account.categoria_default = "test cat"
    mock_account.idioma_default = "es"
    mock_account.duracion_default = 60
    mock_account.formato_default = "shorts"
    
    mock_db.query().filter().first.return_value = mock_account
    mock_db.query().filter().order_by().limit().all.return_value = []
    
    mock_get_db.return_value = mock_db
    
    mock_llm.return_value = {
        "guion": "test guion",
        "titulo_seo": "test title",
        "resumen_para_historial": "test summary",
        "synthetic_content": True
    }

    # Override dependency
    app.dependency_overrides[app.router.dependencies[0].dependency if app.router.dependencies else "get_db"] = lambda: mock_db
    # Simplified override for TestClient:
    from services.script_service.main import get_db
    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.post("/generate-script", json={"account_id": 1, "tema": "test"})
    assert response.status_code == 200
    assert response.json()["guion"] == "test guion"
