from typing import List, Optional, Dict, Any, Union
from motor.core import AgnosticDatabase
from stufio.crud.mongo_base import CRUDMongoBase
from ..models.translation import Translation
from ..schemas.translation import TranslationCreate, TranslationUpdate


class CRUDTranslation(CRUDMongoBase[Translation, TranslationCreate, TranslationUpdate]):
    async def create(self, db: AgnosticDatabase, *, obj_in: TranslationCreate) -> Translation:
        """Create a new translation."""
        translation_dict = obj_in.dict()
        result = await db.i18n_translations.insert_one(translation_dict)
        translation_dict["_id"] = result.inserted_id
        return Translation(**translation_dict)

    async def get(self, db: AgnosticDatabase, translation_id: str) -> Optional[Translation]:
        """Get a translation by ID."""
        translation = await db.i18n_translations.find_one({"_id": translation_id})
        if not translation:
            return None
        return Translation(**translation)

    async def get_all(self, db: AgnosticDatabase, *, skip: int = 0, limit: int = 100) -> List[Translation]:
        """
        Retrieve all translations with optional pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            db: Database connection
            
        Returns:
            List of translations
        """
        cursor = db.i18n_translations.find().skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

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
        cursor = db.i18n_translations.find({"locale": locale}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def update(
        self, db: AgnosticDatabase, *, db_obj: Translation, obj_in: Union[TranslationUpdate, Dict[str, Any]]
    ) -> Optional[Translation]:
        """Update an existing translation."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
            
        updated_translation = await db.i18n_translations.find_one_and_update(
            {"_id": db_obj.id},
            {"$set": update_data},
            return_document=True
        )
        if not updated_translation:
            return None
        return Translation(**updated_translation)

    async def delete(self, db: AgnosticDatabase, *, translation_id: str) -> Optional[Dict[str, str]]:
        """Delete a translation by ID."""
        result = await db.i18n_translations.delete_one({"_id": translation_id})
        if result.deleted_count == 0:
            return None
        return {"detail": "Translation deleted successfully"}


# Create a singleton instance
crud_translation = CRUDTranslation(Translation)
