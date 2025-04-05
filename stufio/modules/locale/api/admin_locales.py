from fastapi import APIRouter, Depends, HTTPException
from typing import List
from stufio.schemas import Msg
from ..models import Locale
from ..crud.crud_locale import crud_locale
from ..schemas import LocaleCreate, LocaleUpdate, LocaleResponse
from stufio.api import deps

router = APIRouter()

@router.post("/locales", response_model=LocaleResponse)
async def create_locale(
    locale: LocaleCreate,
    current_user: str = Depends(deps.get_current_active_superuser)
):
    return await crud_locale.create(locale)


@router.get("/locales", response_model=List[LocaleResponse])
async def read_locales(
    current_user: str = Depends(deps.get_current_active_superuser)
):
    return await crud_locale.get_multi(limit=None)


@router.get("/locales/{locale_id}", response_model=LocaleResponse)
async def read_locale(
    locale_id: str,
    current_user: str = Depends(deps.get_current_active_superuser)
):
    locale = await crud_locale.get(locale_id=locale_id)
    if locale is None:
        raise HTTPException(status_code=404, detail="Locale not found")
    return locale


@router.put("/locales/{locale_id}", response_model=LocaleResponse)
async def update_locale(
    locale_id: str, 
    locale: LocaleUpdate,
    current_user: str = Depends(deps.get_current_active_superuser)
):
    db_obj = await crud_locale.get(locale_id=locale_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Locale not found")
    return await crud_locale.update(db_obj=db_obj, obj_in=locale)


@router.delete("/locales/{locale_id}", response_model=dict)
async def delete_locale(
    locale_id: str,
    current_user: str = Depends(deps.get_current_active_superuser)
):
    result = await crud_locale.delete(locale_id=locale_id)
    if not result:
        raise HTTPException(status_code=404, detail="Locale not found")
    return result
