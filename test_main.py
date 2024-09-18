from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenido a la API de análisis de películas"}

def test_cantidad_filmaciones_mes():
    # Usa el nombre del mes en español
    response = client.get("/cantidad_filmaciones_mes/enero")
    assert response.status_code == 200
    json_response = response.json()
    assert "cantidad" in json_response
    assert isinstance(json_response["cantidad"], int)

def test_datos_unido():
    response = client.get("/datos_unido")
    assert response.status_code == 200
    json_response = response.json()
    assert isinstance(json_response, list) or isinstance(json_response, dict)
    # Si es una lista, verifica que el primer ítem sea un diccionario
    if isinstance(json_response, list) and len(json_response) > 0:
        assert isinstance(json_response[0], dict)

