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

        # Create updated indexes for translations
        await db.command(
            {
                "createIndexes": "i18n_translations",
                "indexes": [
                    {
                        "key": {"key": 1},
                        "name": "translation_key_unique",
                        "unique": True,
                    },
                    {
                        "key": {"modules": 1},
                        "name": "translation_modules_lookup",
                    },
                ],
            }
        )
