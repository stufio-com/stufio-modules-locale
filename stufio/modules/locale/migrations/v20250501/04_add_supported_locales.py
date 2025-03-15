from motor.core import AgnosticDatabase
from stufio.core.migrations.base import MongoMigrationScript
from ...config import LocaleSettings


class AddSupportedLocales(MongoMigrationScript):
    name = "add_supported_locales"
    description = "Add all supported locales from configuration"
    migration_type = "data"
    order = 40

    async def run(self, db: AgnosticDatabase) -> None:
        locales_collection = db.i18n_locales
        locale_settings = LocaleSettings()
        
        # Map of language codes to their full names
        language_names = {
            "en": "English",
            "fr": "French",
            "es": "Spanish",
            "de": "German",
            "pl": "Polish",
            "ru": "Russian",
            "pt": "Portuguese",
            "it": "Italian",
            "nl": "Dutch",
            "dk": "Danish",
            "ua": "Ukrainian",
            "ro": "Romanian",
            "cz": "Czech",
            "se": "Swedish",
            "no": "Norwegian",
            "fi": "Finnish",
            "gr": "Greek",
            "tr": "Turkish",
            "hu": "Hungarian",
            "bg": "Bulgarian",
            "sk": "Slovak",
            "hr": "Croatian",
            "lt": "Lithuanian",
            "lv": "Latvian",
            "ee": "Estonian"
        }

        # Add localized names map
        localized_names = {
            "en": "English",
            "fr": "Français",
            "es": "Español",
            "de": "Deutsch",
            "pl": "Polski",
            "ru": "Русский",
            "pt": "Português",
            "it": "Italiano", 
            "nl": "Nederlands",
            "dk": "Dansk",
            "ua": "Українська",
            "ro": "Română",
            "cz": "Čeština",
            "se": "Svenska",
            "no": "Norsk",
            "fi": "Suomi",
            "gr": "Ελληνικά",
            "tr": "Türkçe",
            "hu": "Magyar",
            "bg": "Български",
            "sk": "Slovenčina",
            "hr": "Hrvatski",
            "lt": "Lietuvių",
            "lv": "Latviešu",
            "ee": "Eesti"
        }

        # Create locales for all supported languages in config
        for code in locale_settings.SUPPORTED_LOCALES:
            name = language_names.get(code, code.upper())
            locale = {
                "code": code,
                "name": name,
                "localized_name": localized_names.get(code, name),
                "details": f"{name} locale",
                "active": True,
                "sort_order": 0
            }
            
            # Insert if not exists
            existing = await locales_collection.find_one({"code": code})
            if not existing:
                await locales_collection.insert_one(locale)