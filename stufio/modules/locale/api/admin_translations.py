from typing import List
from fastapi import APIRouter, Depends, HTTPException
from stufio.schemas import Msg
from stufio.api import deps
from stufio import models
from ..crud.crud_translation import crud_translation
from ..schemas.translation import TranslationCreate, TranslationUpdate, TranslationResponse

router = APIRouter()

@router.post("/translations", response_model=TranslationResponse)
async def create_translation(
    translation: TranslationCreate,
    db = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> TranslationResponse:
    return await crud_translation.create(db=db, obj_in=translation)


@router.get("/translations", response_model=List[TranslationResponse])
async def read_translations(
    skip: int = 0,
    limit: int = 100,
    db = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> List[TranslationResponse]:
    return await crud_translation.get_all(db=db, skip=skip, limit=limit)


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


@router.put("/translations/{translation_id}", response_model=TranslationResponse)
async def update_translation(
    translation_id: str,
    translation: TranslationUpdate,
    db = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> TranslationResponse:
    db_obj = await crud_translation.get(db=db, translation_id=translation_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Translation not found")
    return await crud_translation.update(db=db, db_obj=db_obj, obj_in=translation)


@router.delete("/translations/{translation_id}", response_model=dict)
async def delete_translation(
    translation_id: str,
    db = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> dict:
    result = await crud_translation.delete(db=db, translation_id=translation_id)
    if not result:
        raise HTTPException(status_code=404, detail="Translation not found")
    return result
