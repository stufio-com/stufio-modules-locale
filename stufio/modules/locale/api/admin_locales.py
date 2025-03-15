from fastapi import APIRouter, Depends, HTTPException
from typing import List
from stufio.schemas import Msg
from ..models import Locale
from ..crud import crud_locale
from ..schemas import LocaleResponse
from stufio.api import deps

router = APIRouter()

@router.post("/locales", response_model=Msg)
async def create_locale(locale: Locale, current_user: str = Depends(deps.get_current_active_superuser)):
    await crud_locale.create_locale(locale)
    return Msg(message="Locale created successfully.")


@router.get("/locales", response_model=List[Locale])
async def read_locales(skip: int = 0, limit: int = 100):
    locales = await crud_locale.get_locales(skip=skip, limit=limit)
    return locales


@router.get("/locales/{locale_id}", response_model=LocaleResponse)
async def read_locale(locale_id: str, current_user: str = Depends(deps.get_current_active_superuser)):
    locale = await crud_locale.get_locale(locale_id)
    if locale is None:
        raise HTTPException(status_code=404, detail="Locale not found")
    return locale


@router.put("/locales/{locale_id}", response_model=Msg)
async def update_locale(locale_id: str, locale: Locale, current_user: str = Depends(deps.get_current_active_superuser)):
    updated_locale = await crud_locale.update_locale(locale_id, locale)
    if updated_locale is None:
        raise HTTPException(status_code=404, detail="Locale not found")
    return Msg(message="Locale updated successfully.")


@router.delete("/locales/{locale_id}", response_model=Msg)
async def delete_locale(locale_id: str, current_user: str = Depends(deps.get_current_active_superuser)):
    deleted = await crud_locale.delete_locale(locale_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Locale not found")
    return Msg(message="Locale deleted successfully.")
