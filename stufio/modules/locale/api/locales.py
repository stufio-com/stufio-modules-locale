from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas.locale import LocaleResponse
from ..crud.crud_locale import get_locale, get_all_locales, get_active_locales
from stufio.api import deps

router = APIRouter()


@router.get("/locales", response_model=List[LocaleResponse])
async def list_locales(db=Depends(deps.get_db)):
    return await get_active_locales(db=db)


@router.get("/locales/{locale_id}", response_model=LocaleResponse)
async def read_locale(locale_id: str, db=Depends(deps.get_db)):
    locale = await get_locale(db=db, locale_id=locale_id)
    if not locale:
        raise HTTPException(status_code=404, detail="Locale not found")
    return locale
