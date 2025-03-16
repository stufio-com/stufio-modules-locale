from typing import List, Optional, Dict, Any, Union
from motor.core import AgnosticDatabase
from stufio.crud.mongo_base import CRUDMongoBase
from ..models.translation import Translation
from ..schemas.translation import TranslationCreate, TranslationUpdate


class CRUDTranslation(CRUDMongoBase[Translation, TranslationCreate, TranslationUpdate]):

    async def get_by_locale(self, db: AgnosticDatabase, locale: str, *, skip: int = 0, limit: int = 100) -> List[Translation]:
        """
        Retrieve all translations for a specific locale.
        
        Args:
            locale: The locale code to filter translations by (e.g., 'en', 'fr')
            skip: Number of records to skip
            limit: Maximum number of records to return
            db: Database connection
            
        Returns:
            List of Translation objects for the specified locale
        """
        return await crud_translation.get_multi(db=db, filter_expression=Translation.locale == locale, skip=skip, limit=limit)


# Create a singleton instance
crud_translation = CRUDTranslation(Translation)
