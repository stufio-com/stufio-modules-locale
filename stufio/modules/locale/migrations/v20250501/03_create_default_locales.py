from motor.core import AgnosticDatabase
from stufio.core.migrations.base import MongoMigrationScript
from odmantic import AIOEngine
from stufio.db.mongo import get_engine
from ...models.locale import Locale


class CreateDefaultLocales(MongoMigrationScript):
    name = "create_default_locales"
    description = "Initialize the system with default locales"
    migration_type = "data"
    order = 30

    async def run(self, db: AgnosticDatabase) -> None:
        engine = get_engine()

        # "en", "fr", "es", "de", "pl", "ru"
        default_locales = [
            Locale(
                code="en",
                name="English",
                localized_name="English",
                details="English language",
                active=True,
                sort_order=0
            ),
            Locale(
                code="es",
                name="Spanish", 
                localized_name="Español",
                details="Spanish language",
                active=True,
                sort_order=0
            ),
            Locale(
                code="fr",
                name="French",
                localized_name="Français",
                details="French language",
                active=True,
                sort_order=0
            ),
            Locale(
                code="de",
                name="German",
                localized_name="Deutsch",
                details="German language",
                active=True,
                sort_order=0
            ),
            Locale(
                code="pl",
                name="Polish",
                localized_name="Polski",
                details="Polish language",
                active=True,
                sort_order=0
            ),
            Locale(
                code="ru",
                name="Russian",
                localized_name="Русский",
                details="Russian language",
                active=True,
                sort_order=0
            ),
        ]

        # Insert default locales if they do not exist
        for locale in default_locales:
            existing = await engine.find_one(Locale, Locale.code == locale.code)
            if not existing:
                await engine.save(locale)
