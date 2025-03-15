from typing import List
from fastapi import APIRouter, Depends
from stufio.schemas import Msg
from stufio.api import deps
from stufio import models
from ..crud import crud_translation
from ..models import Translation
from ..schemas import TranslationCreate, TranslationUpdate

router = APIRouter()

@router.post("/translations", response_model=Msg)
async def create_translation(
    translation: TranslationCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Msg:
    await crud_translation.create_translation(translation)
    return {"msg": "Translation created successfully"}


@router.get("/translations", response_model=List[Translation])
async def read_translations(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> List[Translation]:
    return await crud_translation.get_translations(skip=skip, limit=limit)


@router.get("/translations/{translation_id}", response_model=Translation)
async def read_translation(
    translation_id: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Translation:
    return await crud_translation.get_translation(translation_id)


@router.put("/translations/{translation_id}", response_model=Msg)
async def update_translation(
    translation_id: str,
    translation: TranslationUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Msg:
    await crud_translation.update_translation(translation_id, translation)
    return {"msg": "Translation updated successfully"}


@router.delete("/translations/{translation_id}", response_model=Msg)
async def delete_translation(
    translation_id: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Msg:
    await crud_translation.delete_translation(translation_id)
    return {"msg": "Translation deleted successfully"}
