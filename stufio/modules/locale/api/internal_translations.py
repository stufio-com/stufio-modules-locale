from typing import Optional
from fastapi import APIRouter, Depends, Body, HTTPException
from ..schemas.translation import (
    TranslationCreate, 
    TranslationUpdate, 
    TranslationResponse,
)
from ..crud.crud_translation import crud_translation
from ..services.cache_service import cache_translations, cache_module_translations
from stufio.api import deps


router = APIRouter()


@router.post("/translations", response_model=TranslationResponse)
async def create_translation(
    key: str = Body(...),
    locale: str = Body(...),
    module: str = Body(...),
    text: Optional[str] = Body(None),
    description: Optional[str] = Body(None),
    db=Depends(deps.get_db),
) -> TranslationResponse:
    """
    Create a new translation.
    """
    # Ensure at least one module is specified
    if not module or len(module) == 0:
        raise HTTPException(status_code=400, detail="At least one module must be specified")

    # Create the translation
    translation_in = TranslationCreate(
        key=key,
        modules=[module],
        description=description if description else None,
    )
    
    if text and text != key:
        translation_in.translations = {locale: {"text": text}}

    # Check if translation key already exists
    existing = await crud_translation.get_by_key(db=db, key=translation_in.key)
    if existing:
        # Check for new modules and add them to existing.modules if any
        new_modules = set(translation_in.modules) - set(existing.modules)
        if new_modules:
            existing.modules.extend(new_modules)
            result = await crud_translation.update(db=db, db_obj=existing, obj_in={"modules": existing.modules})
        else:
            raise HTTPException(status_code=400, detail=f"Translation with key '{translation_in.key}' already exists for all specified modules")
    else:
        # Create the translation
        result = await crud_translation.create(db=db, obj_in=translation_in)

        # Invalidate cache for all affected locales and modules
        if translation_in.translations:
            for locale in translation_in.translations.keys():
                await cache_translations(locale)
                for module in translation_in.modules:
                    await cache_module_translations(locale, module)

    return result


@router.put("/translations", response_model=TranslationResponse)
async def update_translation(
    update_in: TranslationUpdate,
    key: str = Body(...),
    db=Depends(deps.get_db),
) -> TranslationResponse:
    """
    Update a translation by key.
    """
    # Find the translation
    translation = await crud_translation.get_by_key(db=db, key=key)
    if not translation:
        raise HTTPException(status_code=404, detail=f"Translation with key '{key}' not found")
    
    # Ensure modules list is not emptied
    if update_in.modules is not None and len(update_in.modules) == 0:
        raise HTTPException(status_code=400, detail="At least one module must be specified")
    
    
    # Update the translation
    result = await crud_translation.update(db=db, db_obj=translation, obj_in=update_in)
    
    # Invalidate cache for affected locales
    if update_in.translations:
        for locale in update_in.translations.keys():
            await cache_translations(locale)
            # Invalidate all modules this translation might apply to
            modules = update_in.modules or translation.modules
            for module in modules:
                await cache_module_translations(locale, module)
    
    return result
