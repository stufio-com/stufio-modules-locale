from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from stufio.schemas import Msg
from stufio.api import deps
from stufio import models
from ..crud.crud_translation import crud_translation
from ..schemas.translation import (
    TranslationCreate, 
    TranslationUpdate, 
    TranslationResponse,
    LocaleTranslationUpdate,
)
from ..services.cache_service import cache_translations, cache_module_translations

router = APIRouter()

@router.get("/translations", response_model=List[TranslationResponse])
async def read_translations(
    skip: int = 0,
    limit: int = 100,
    module: Optional[str] = None,
    locale: Optional[str] = None,
    db = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> List[TranslationResponse]:
    """
    Get all translations with optional filters.
    """
    if module and locale:
        # Get translations for specific module and locale
        raw_filter = {
            "modules": module,
            f"translations.{locale}": {"$exists": True}
        }
        return await crud_translation.get_multi(db=db, filter=raw_filter, skip=skip, limit=limit)
    elif module:
        # Get translations for specific module
        return await crud_translation.get_multi_by_fields(db=db, fields={"modules": module}, skip=skip, limit=limit)
    elif locale:
        # Get translations for specific locale
        return await crud_translation.get_by_locale(db=db, locale=locale, skip=skip, limit=limit)
    else:
        # Get all translations
        return await crud_translation.get_multi(db=db, skip=skip, limit=limit)

@router.post("/translations", response_model=TranslationResponse)
async def create_translation(
    translation_in: TranslationCreate,
    db = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> TranslationResponse:
    """
    Create a new translation.
    """
    # Check if the key already exists
    existing = await crud_translation.get_by_key(db=db, key=translation_in.key)
    if existing:
        raise HTTPException(status_code=400, detail=f"Translation with key '{translation_in.key}' already exists")
    
    # Ensure at least one module is specified
    if not translation_in.modules or len(translation_in.modules) == 0:
        raise HTTPException(status_code=400, detail="At least one module must be specified")
        
    # Create the translation
    result = await crud_translation.create(db=db, obj_in=translation_in)
    
    # Invalidate cache for affected locales and modules
    if translation_in.translations:
        for locale in translation_in.translations.keys():
            await cache_translations(locale)
            for module in translation_in.modules:
                await cache_module_translations(locale, module)
    
    return result

@router.get("/translations/{id}", response_model=TranslationResponse)
async def read_translation_by_id(
    id: str,
    db = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> TranslationResponse:
    """
    Get a specific translation by ID.
    """
    translation = await crud_translation.get(db=db, id=id)
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    return translation

@router.post("/translations/by-key", response_model=TranslationResponse)
async def get_translation_by_key(
    key: str = Body(...),
    db = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> TranslationResponse:
    """
    Get a specific translation by key.
    """
    translation = await crud_translation.get_by_key(db=db, key=key)
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    return translation

@router.put("/translations/{id}", response_model=TranslationResponse)
async def update_translation(
    id: str,
    translation_in: TranslationUpdate,
    db = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> TranslationResponse:
    """
    Update a translation.
    """
    # Find the translation
    translation = await crud_translation.get(db=db, id=id)
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
        
    # Ensure modules list is not emptied
    if translation_in.modules is not None and len(translation_in.modules) == 0:
        raise HTTPException(status_code=400, detail="At least one module must be specified")
    
    # Update the translation
    result = await crud_translation.update(db=db, db_obj=translation, obj_in=translation_in)
    
    # Invalidate cache for affected locales and modules
    if translation_in.translations:
        for locale in translation_in.translations.keys():
            await cache_translations(locale)
            # Invalidate all modules this translation might apply to
            modules = translation_in.modules or translation.modules
            for module in modules:
                await cache_module_translations(locale, module)
    
    return result

@router.delete("/translations/{id}", response_model=Dict[str, bool])
async def delete_translation(
    id: str,
    db = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Dict[str, bool]:
    """
    Delete a translation by ID.
    """
    translation = await crud_translation.get(db=db, id=id)
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    
    # Invalidate cache for affected locales and modules
    for locale in translation.translations.keys():
        await cache_translations(locale)
        for module in translation.modules:
            await cache_module_translations(locale, module)
        
    # Delete the translation
    result = await crud_translation.delete(db=db, id=id)
    return {"success": result}

@router.post("/translations/locale", response_model=TranslationResponse)
async def upsert_translation_locale(
    key: str = Body(...),
    locale: str = Body(...),
    text: str = Body(...),
    modules: List[str] = Body(...),
    description: Optional[str] = Body(None),
    module_overrides: Optional[Dict[str, str]] = Body(None),
    db = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> TranslationResponse:
    """
    Create or update a single locale for a translation.
    """
    result = await crud_translation.upsert_translation(
        db=db,
        key=key,
        modules=modules,
        locale=locale,
        text=text,
        description=description,
        module_override=module_overrides,
    )
    
    # Invalidate cache
    await cache_translations(locale)
    for module in modules:
        await cache_module_translations(locale, module)
        
    return result

@router.post("/translations/delete-locale", response_model=Dict[str, bool])
async def delete_locale_translation(
    key: str = Body(...),
    locale: str = Body(...),
    db = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Dict[str, bool]:
    """
    Remove a specific locale from a translation.
    """
    translation = await crud_translation.get_by_key(db=db, key=key)
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
        
    result = await crud_translation.delete_locale_translation(db=db, key=key, locale=locale)
    if not result:
        raise HTTPException(status_code=404, detail="Locale not found in translation")
    
    # Invalidate cache
    await cache_translations(locale)
    for module in translation.modules:
        await cache_module_translations(locale, module)
        
    return {"deleted": True}
