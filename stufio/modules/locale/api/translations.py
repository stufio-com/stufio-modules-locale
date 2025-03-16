from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from ..schemas.translation import TranslationCreate, TranslationUpdate, TranslationResponse
from ..crud.crud_translation import crud_translation
from ..services.cache_service import cache_translations
from stufio import models
from stufio.api import deps

router = APIRouter()

@router.post("/translations", response_model=TranslationResponse)
async def create_new_translation(
    translation: TranslationCreate,
    db = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> TranslationResponse:
    new_translation = await crud_translation.create(db=db, obj_in=translation)
    await cache_translations(new_translation.locale)
    return new_translation

@router.get("/translations/{translation_id}", response_model=TranslationResponse)
async def read_translation(
    translation_id: str,
    db = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> TranslationResponse:
    translation = await crud_translation.get(db=db, translation_id=translation_id)
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    return translation

@router.get("/translations/locale/{locale}", response_model=List[TranslationResponse])
async def read_translations_by_locale(
    locale: str,
    db = Depends(deps.get_db),
) -> List[TranslationResponse]:
    translations = await crud_translation.get_by_locale(db=db, locale=locale)
    return translations

@router.put("/translations/{translation_id}", response_model=TranslationResponse)
async def update_existing_translation(
    translation_id: str,
    translation: TranslationUpdate,
    db = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> TranslationResponse:
    db_obj = await crud_translation.get(db=db, translation_id=translation_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Translation not found")
    updated_translation = await crud_translation.update(db=db, db_obj=db_obj, obj_in=translation)
    await cache_translations(updated_translation.locale)
    return updated_translation

@router.delete("/translations/{translation_id}", response_model=dict)
async def delete_existing_translation(
    translation_id: str,
    db = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> dict:
    result = await crud_translation.delete(db=db, translation_id=translation_id)
    if not result:
        raise HTTPException(status_code=404, detail="Translation not found")
    return result
