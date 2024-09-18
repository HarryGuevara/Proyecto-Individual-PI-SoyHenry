from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenido a la API de análisis de películas"}

def test_cantidad_filmaciones_mes():
    response = client.get("/cantidad_filmaciones_mes/january")
    assert response.status_code == 200
    assert "cantidad" in response.json()

def test_datos_unido():
    response = client.get("/datos_unido")
    assert response.status_code == 200
    assert isinstance(response.json(), list) or isinstance(response.json(), dict)
