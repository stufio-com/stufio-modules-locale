from fastapi.testclient import TestClient
from stufio.modules.locale.api.locales import router as locales_router
from stufio.modules.locale.crud.crud_locale import crud_locale
from stufio.modules.locale.models.locale import Locale
from stufio.modules.locale.schemas.locale import LocaleCreate, LocaleUpdate

client = TestClient(locales_router)

def test_create_locale():
    response = client.post("/locales/", json={"name": "en", "details": "English"})
    assert response.status_code == 201
    assert response.json()["name"] == "en"

def test_read_locale():
    response = client.get("/locales/en")
    assert response.status_code == 200
    assert response.json()["name"] == "en"

def test_update_locale():
    response = client.put("/locales/en", json={"name": "en", "details": "Updated English"})
    assert response.status_code == 200
    assert response.json()["details"] == "Updated English"

def test_delete_locale():
    response = client.delete("/locales/en")
    assert response.status_code == 204
    response = client.get("/locales/en")
    assert response.status_code == 404

def test_get_all_locales():
    response = client.get("/locales/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Ensure it returns a list of locales