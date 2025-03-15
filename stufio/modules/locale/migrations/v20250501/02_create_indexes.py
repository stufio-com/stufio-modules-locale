from motor.core import AgnosticDatabase
from stufio.core.migrations.base import MongoMigrationScript


class CreateIndexes(MongoMigrationScript):
    name = "create_indexes"
    description = "Create indexes for locale module collections"
    migration_type = "schema"
    order = 20

    async def run(self, db: AgnosticDatabase) -> None:
        # Create indexes for the locales collection
        await db.command({
            "createIndexes": "i18n_locales",
            "indexes": [
                {
                    "key": {"code": 1},
                    "name": "locale_code_lookup",
                    "unique": True
                },
                {
                    "key": {"name": 1},
                    "name": "locale_name_lookup"
                }
            ]
        })

        # Create indexes for the translations collection
        await db.command({
            "createIndexes": "i18n_translations",
            "indexes": [
                {
                    "key": {"module_name": 1},
                    "name": "translation_module_lookup"
                },
                {
                    "key": {"key": 1, "locale": 1, "module_name": 1},
                    "name": "translation_unique_key",
                    "unique": True
                }
            ]
        })