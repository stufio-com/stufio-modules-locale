from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from ..schemas.translation import TranslationCreate, TranslationUpdate, TranslationResponse
from ..crud.crud_translation import (
    create_translation,
    get_translation,
    get_translations_by_locale,
    update_translation,
    delete_translation,
)
from ..services.cache_service import cache_translations
from stufio import models
from stufio.api import deps

router = APIRouter()

@router.post("/translations", response_model=TranslationResponse)
async def create_new_translation(
    translation: TranslationCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> TranslationResponse:
    new_translation = await create_translation(translation)
    await cache_translations(new_translation.locale)
    return new_translation

@router.get("/translations/{translation_id}", response_model=TranslationResponse)
async def read_translation(
    translation_id: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> TranslationResponse:
    translation = await get_translation(translation_id)
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    return translation

@router.get("/translations/locale/{locale}", response_model=List[TranslationResponse])
async def read_translations_by_locale(
    locale: str,
) -> List[TranslationResponse]:
    translations = await get_translations_by_locale(locale)
    return translations

@router.put("/translations/{translation_id}", response_model=TranslationResponse)
async def update_existing_translation(
    translation_id: str,
    translation: TranslationUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> TranslationResponse:
    updated_translation = await update_translation(translation_id, translation)
    if not updated_translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    await cache_translations(updated_translation.locale)
    return updated_translation

@router.delete("/translations/{translation_id}", response_model=TranslationResponse)
async def delete_existing_translation(
    translation_id: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> TranslationResponse:
    deleted_translation = await delete_translation(translation_id)
    if not deleted_translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    return deleted_translation
