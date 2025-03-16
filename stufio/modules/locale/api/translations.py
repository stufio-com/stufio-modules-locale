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
    """
    Create a new translation.
    """
    new_translation = await crud_translation.create(db=db, obj_in=translation)
    await cache_translations(new_translation.locale)
    return new_translation

@router.get("/translations/locale/{locale}", response_model=List[TranslationResponse])
async def read_translations_by_locale(
    locale: str,
    db = Depends(deps.get_db),
) -> List[TranslationResponse]:
    """
    Retrieve all translations for a specific locale.
    """
    translations = await crud_translation.get_by_locale(db=db, locale=locale)
    return translations

