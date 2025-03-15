from motor.core import AgnosticDatabase
from stufio.core.migrations.base import MongoMigrationScript


class CreateDefaultLocales(MongoMigrationScript):
    name = "create_default_locales"
    description = "Initialize the system with default locales"
    migration_type = "data"
    order = 30

    async def run(self, db: AgnosticDatabase) -> None:
        locales_collection = db.i18n_locales

        # "en", "fr", "es", "de", "pl", "ru"
        default_locales = [
            {"name": "English", "code": "en", "localized_name": "English", "details": "English", "active": True, "sort_order": 0},
            {"name": "Spanish", "code": "es", "localized_name": "Español", "details": "Spanish", "active": True, "sort_order": 0},
            {"name": "French", "code": "fr", "localized_name": "Français", "details": "French", "active": True, "sort_order": 0},
            {"name": "German", "code": "de", "localized_name": "Deutsch", "details": "German", "active": True, "sort_order": 0},
            {"name": "Polish", "code": "pl", "localized_name": "Polski", "details": "Polish", "active": True, "sort_order": 0},
            {"name": "Russian", "code": "ru", "localized_name": "Русский", "details": "Russian", "active": True, "sort_order": 0},
        ]

        # Insert default locales if they do not exist
        for locale in default_locales:
            existing = await locales_collection.find_one({"code": locale["code"]})
            if not existing:
                await locales_collection.insert_one(locale)
