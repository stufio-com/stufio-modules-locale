from celery.worker.control import active
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from ..schemas.locale import LocaleResponse
from ..models.locale import Locale
from ..crud.crud_locale import crud_locale
from stufio.api import deps

router = APIRouter()


@router.get("/locales", response_model=List[LocaleResponse])
async def list_locales(db = Depends(deps.get_db)):
    return await crud_locale.get_multi(
        db=db, filter_expression=Locale.active == True, skip=0, limit=None
    )


@router.get("/locales/{locale_id}", response_model=LocaleResponse)
async def read_locale(locale_id: str, db = Depends(deps.get_db)):
    locale = await crud_locale.get(db=db, id=locale_id)
    if not locale:
        raise HTTPException(status_code=404, detail="Locale not found")
    return locale
