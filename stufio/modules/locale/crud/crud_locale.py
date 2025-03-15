from typing import List
from motor.core import AgnosticDatabase
from ..models.locale import Locale
from ..schemas.locale import LocaleCreate, LocaleUpdate
from stufio.api.deps import get_db
from fastapi import HTTPException, Depends


async def create_locale(
    locale: LocaleCreate, db: AgnosticDatabase = Depends(get_db)
) -> Locale:
    existing_locale = await db.i18n_locales.find_one({"name": locale.name})
    if existing_locale:
        raise HTTPException(status_code=400, detail="Locale already exists")
    new_locale = await db.i18n_locales.insert_one(locale.dict())
    return await db.i18n_locales.find_one({"_id": new_locale.inserted_id})


async def get_locale(locale_id: str, db: AgnosticDatabase = Depends(get_db)) -> Locale:
    locale = await db.i18n_locales.find_one({"_id": locale_id})
    if not locale:
        raise HTTPException(status_code=404, detail="Locale not found")
    return locale


async def get_all_locales(
    skip: int = 0, limit: int = 100, db: AgnosticDatabase = Depends(get_db)
) -> List[Locale]:
    """
    Retrieve all locales with optional pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database connection
        
    Returns:
        List of locales
    """
    cursor = db.i18n_locales.find().skip(skip).limit(limit)
    return await cursor.to_list(length=limit)


async def get_active_locales(
    skip: int = 0, limit: int = 100, db: AgnosticDatabase = Depends(get_db)
) -> List[Locale]:
    """
    Retrieve only active locales with optional pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database connection
        
    Returns:
        List of active locales
    """
    cursor = db.i18n_locales.find({"active": True}).sort([("sort_order", 1), ("name", 1)]).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)


async def update_locale(
    locale_id: str, locale: LocaleUpdate, db: AgnosticDatabase = Depends(get_db)
) -> Locale:
    updated_locale = await db.i18n_locales.find_one_and_update(
        {"_id": locale_id},
        {"$set": locale.dict(exclude_unset=True)},
        return_document=True
    )
    if not updated_locale:
        raise HTTPException(status_code=404, detail="Locale not found")
    return updated_locale


async def delete_locale(locale_id: str, db: AgnosticDatabase = Depends(get_db)) -> dict:
    result = await db.i18n_locales.delete_one({"_id": locale_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Locale not found")
    return {"detail": "Locale deleted successfully"}
