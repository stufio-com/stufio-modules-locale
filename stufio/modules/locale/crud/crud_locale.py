from typing import List, Optional, Dict, Any, Union
from motor.core import AgnosticDatabase
from ..models.locale import Locale
from ..schemas.locale import LocaleCreate, LocaleUpdate
from stufio.crud.mongo_base import CRUDMongoBase


class CRUDLocale(CRUDMongoBase[Locale, LocaleCreate, LocaleUpdate]):
    async def create(self, db: AgnosticDatabase, *, obj_in: LocaleCreate) -> Optional[Locale]:
        existing_locale = await db.i18n_locales.find_one({"name": obj_in.name})
        if existing_locale:
            return None

        locale_data = obj_in.dict()
        new_locale = await db.i18n_locales.insert_one(locale_data)
        return await db.i18n_locales.find_one({"_id": new_locale.inserted_id})

    async def get(self, db: AgnosticDatabase, locale_id: str) -> Optional[Locale]:
        locale = await db.i18n_locales.find_one({"_id": locale_id})
        if not locale:
            return None
        return locale

    async def get_all(self, db: AgnosticDatabase, *, skip: int = 0, limit: int = 100) -> List[Locale]:
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

    async def get_active(self, db: AgnosticDatabase, *, skip: int = 0, limit: int = 100) -> List[Locale]:
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

    async def update(
        self, db: AgnosticDatabase, *, db_obj: Locale, obj_in: Union[LocaleUpdate, Dict[str, Any]]
    ) -> Optional[Locale]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        updated_locale = await db.i18n_locales.find_one_and_update(
            {"_id": db_obj.id},
            {"$set": update_data},
            return_document=True
        )
        if not updated_locale:
            return None
        return updated_locale

    async def delete(self, db: AgnosticDatabase, *, locale_id: str) -> Optional[Dict[str, str]]:
        result = await db.i18n_locales.delete_one({"_id": locale_id})
        if result.deleted_count == 0:
            return None
        return {"detail": "Locale deleted successfully"}


# Create a singleton instance
crud_locale = CRUDLocale(Locale)
