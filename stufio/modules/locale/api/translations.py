from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from ..schemas.translation import TranslationResponse
from ..crud.crud_translation import crud_translation
from ..services.cache_service import cache_service
from stufio.api import deps
from stufio.db.redis import RedisClient

import json

router = APIRouter()


@router.get("/translations/locale/{locale}", response_model=Dict[str, str])
async def read_translations_by_locale(
    locale: str,
    module: str,
    skip: Optional[int] = 0,
    limit: Optional[int] = None,
    db = Depends(deps.get_db),
) -> List[TranslationResponse]:
    """
    Retrieve all translations for a specific locale.
    """
    
    # Check cache first
    cache_key = f"translations_map:{locale}:{module}"
    redis = await RedisClient()
    cached = await redis.get(cache_key)

    if cached:
        try:
            return json.loads(cached)
        except:
            # If cache parse fails, continue to get from DB
            pass

    # Get translations map from database
    result = await crud_translation.get_translations_map(
        db=db, locale=locale, module_name=module, skip=skip, limit=limit
    )

    # Cache for 5 minutes
    if result:
        await redis.set(cache_key, json.dumps(result), ex=300)
        
    return result


@router.post("/translations/text", response_model=Dict[str, str])
async def get_translation_text(
    key: str = Body(...),
    locale: str = Body(...),
    module: Optional[str] = Body(None),
    db = Depends(deps.get_db),
) -> Dict[str, str]:
    """
    Get just the text for a specific translation, locale, and optional module.
    """
    # Try to get from cache first
    cached = await cache_service.get_translation(locale, key, module)
    
    if cached:
        return {"text": cached}
    
    # Get from database with possible module override
    text = await crud_translation.get_translation(
        db=db, key=key, locale=locale, module_name=module
    )
    
    if text is None:
        raise HTTPException(status_code=404, detail="Translation not found")
    
    # Cache the result
    await cache_service.set_translation(locale, key, text, module)
    
    return {"text": text}
