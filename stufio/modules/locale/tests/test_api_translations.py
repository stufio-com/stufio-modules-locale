from fastapi.testclient import TestClient
from stufio.modules.locale.api.translations import router as translations_router
from stufio.modules.locale.crud.crud_translation import crud_translation
from stufio.modules.locale.models.translation import Translation
from stufio.modules.locale.schemas.translation import TranslationCreate, TranslationUpdate

client = TestClient(translations_router)

def test_create_translation():
    translation_data = {
        "module_name": "test_module",
        "key": "greeting",
        "value": "Hello",
        "locale": "en",
        "details": "A greeting message"
    }
    response = client.post("/translations/", json=translation_data)
    assert response.status_code == 201
    assert response.json()["key"] == translation_data["key"]

def test_read_translation():
    response = client.get("/translations/en/test_module/greeting")
    assert response.status_code == 200
    assert response.json()["value"] == "Hello"

def test_update_translation():
    update_data = {
        "value": "Hello, World!"
    }
    response = client.put("/translations/en/test_module/greeting", json=update_data)
    assert response.status_code == 200
    assert response.json()["value"] == update_data["value"]

def test_delete_translation():
    response = client.delete("/translations/en/test_module/greeting")
    assert response.status_code == 204
    response = client.get("/translations/en/test_module/greeting")
    assert response.status_code == 404

def test_get_translations_by_locale():
    response = client.get("/translations/en/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Expecting a list of translations