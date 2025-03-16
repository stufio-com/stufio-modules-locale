from gc import callbacks
from operator import call
from typing import List, Optional, Dict, Any, Union
from motor.core import AgnosticDatabase
from ..models.locale import Locale
from ..schemas.locale import LocaleCreate, LocaleUpdate
from stufio.crud.mongo_base import CRUDMongoBase


class CRUDLocale(CRUDMongoBase[Locale, LocaleCreate, LocaleUpdate]):

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
        return await cursor.to_list(length=limit, callbacks=lambda x: Locale(**x))


# Create a singleton instance
crud_locale = CRUDLocale(Locale)
