from fastapi import HTTPException, Depends
from motor.core import AgnosticDatabase
from stufio.api.deps import get_db
from stufio.modules.locale.models.translation import Translation
from stufio.modules.locale.schemas.translation import TranslationCreate, TranslationUpdate


async def create_translation(
    translation: TranslationCreate, db: AgnosticDatabase = Depends(get_db)
) -> Translation:
    translation_dict = translation.dict()
    result = await db.translations.insert_one(translation_dict)
    translation_dict["_id"] = result.inserted_id
    return Translation(**translation_dict)


async def get_translation(
    translation_id: str, db: AgnosticDatabase = Depends(get_db)
) -> Translation:
    translation = await db.translations.find_one({"_id": translation_id})
    if translation is None:
        raise HTTPException(status_code=404, detail="Translation not found")
    return Translation(**translation)


async def update_translation(
    translation_id: str,
    translation: TranslationUpdate,
    db: AgnosticDatabase = Depends(get_db),
) -> Translation:
    translation_dict = translation.dict(exclude_unset=True)
    await db.translations.update_one({"_id": translation_id}, {"$set": translation_dict})
    return await get_translation(translation_id)


async def delete_translation(
    translation_id: str, db: AgnosticDatabase = Depends(get_db)
) -> dict:
    result = await db.translations.delete_one({"_id": translation_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Translation not found")
    return {"message": "Translation deleted"}

async def get_translations_by_locale(
    locale: str, db: AgnosticDatabase = Depends(get_db)
) -> list[Translation]:
    """
    Retrieve all translations for a specific locale.
    
    Args:
        locale: The locale code to filter translations by (e.g., 'en', 'fr')
        
    Returns:
        List of Translation objects for the specified locale
    """
    cursor = db.i18n_translations.find({"locale": locale})
    translations = []
    async for doc in cursor:
        translations.append(Translation(**doc))
    return translations
