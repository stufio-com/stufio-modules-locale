from operator import call
from typing import Dict, List, Optional, Any
from motor.core import AgnosticDatabase
from datetime import datetime, timezone

from ..models.translation import Translation, LocaleTranslation
from ..schemas.translation import LocaleTranslationCreate, TranslationCreate, TranslationUpdate
from stufio.crud.mongo_base import CRUDMongo


class CRUDTranslation(CRUDMongo[Translation, TranslationCreate, TranslationUpdate]):
    async def get_by_locale(
        self,
        locale: str,
        module_name: Optional[str] = None,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Translation]:
        """
        Retrieve all translations that have a specific locale.
        
        Args:
            locale: The locale code to filter translations by (e.g., 'en', 'fr')
            module_name: Optional module name filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Translation objects for the specified locale
        """
        # Build filter for translations that have the specified locale
        raw_filter = {}

        # Add module filter if specified
        if module_name:
            raw_filter["modules"] = module_name

        return await self.get_multi(filters=raw_filter, skip=skip, limit=limit)

    async def get_by_key(self, key: str) -> Optional[Translation]:
        """Get a translation by its key."""
        return await self.get_by_field(field="key", value=key)

    async def get_by_module(self, module_name: str) -> List[Translation]:
        """Get all translations for a specific module."""
        return await self.get_multi(filters={"modules": module_name})

    async def get_translation(
        self, key: str, locale: str, module_name: Optional[str] = None
    ) -> Optional[str]:
        """
        Get a specific translation text by key and locale, with optional module override.
        
        Args:
            key: Translation key
            locale: Locale code
            module_name: Optional module to check for overrides
            
        Returns:
            Translation text or None if not found
        """
        translation = await self.get_by_key(key=key)
        if not translation:
            return None

        if  locale not in translation.translations:
            return translation.key

        # Get the locale translation
        locale_trans = translation.translations[locale]

        # Check for module override if module is specified
        if module_name and module_name in locale_trans.module_overrides:
            return locale_trans.module_overrides[module_name]

        # Otherwise return the default text
        return locale_trans.text

    async def upsert_translation(
        self,
        key: str,
        modules: List[str],
        translations: Optional[Dict[str, LocaleTranslationCreate]] = None,
        locale: Optional[str] = None,
        text: Optional[str] = None,
        description: Optional[str] = None,
        module_override: Optional[Dict[str, str]] = None,
    ) -> Translation:
        """
        Create or update a translation.
        
        You can either:
        1. Pass a dictionary of translations to update/create multiple locales at once
        2. Pass locale and text to update a single locale translation
        
        Args:
            key: The translation key
            modules: List of modules this translation belongs to
            translations: Dictionary of locale translations to update
            locale: Single locale to update (if not using translations dict)
            text: Translation text for the single locale
            description: Optional description for the translation key
            module_override: Optional module-specific override for the locale
            
        Returns:
            Updated Translation object
        """
        # Try to find existing translation
        translation = await self.get_by_key(key=key)
        now = datetime.now(timezone.utc)

        if not translation:
            # Create new translation
            translation_data = {
                "key": key,
                "modules": modules,
                "created_at": now,
                "updated_at": now,
                "translations": {},
            }

            if description:
                translation_data["description"] = description

            translation = Translation(**translation_data)
        else:
            # Update timestamp
            translation.updated_at = now

            # Update modules if provided
            if modules:
                translation.modules = list(set(modules))  # Ensure unique values

            # Update description if provided
            if description is not None:
                translation.description = description

        # Handle bulk translations update
        if translations:
            for locale_code, locale_trans in translations.items():
                # Check if locale already exists
                if locale_code in translation.translations:
                    # Update existing locale translation
                    locale_translation = translation.translations[locale_code]
                    locale_translation.text = locale_trans.text
                    locale_translation.updated_at = now

                    # Update module overrides if provided
                    if locale_trans.module_overrides:
                        for module, override_text in locale_trans.module_overrides.items():
                            locale_translation.module_overrides[module] = override_text
                else:
                    # Add new locale translation
                    translation.translations[locale_code] = LocaleTranslation(
                        text=locale_trans.text,
                        module_overrides=locale_trans.module_overrides or {},
                        created_at=now,
                        updated_at=now
                    )

        # Handle single locale update
        elif locale and text is not None:
            if locale in translation.translations:
                # Update existing locale
                locale_translation = translation.translations[locale]
                locale_translation.text = text
                locale_translation.updated_at = now

                # Add module override if provided
                if module_override:
                    for module, override_text in module_override.items():
                        locale_translation.module_overrides[module] = override_text
            else:
                # Add new locale
                translation.translations[locale] = LocaleTranslation(
                    text=text,
                    module_overrides=module_override or {},
                    created_at=now,
                    updated_at=now
                )

        # Save translation
        return await self.engine.save(translation)

    async def upsert_module_override(
        self,
        key: str,
        locale: str,
        module_name: str,
        text: str,
    ) -> Translation:
        """
        Set a module-specific override for a translation.
        
        Args:
            key: Translation key
            locale: Locale code
            module_name: Module name for the override
            text: Override text
            
        Returns:
            Updated Translation object
        """
        translation = await self.get_by_key(key=key)

        if not translation:
            raise ValueError(f"Translation with key '{key}' not found")

        if locale not in translation.translations:
            raise ValueError(f"Locale '{locale}' not found in translation '{key}'")

        # Ensure module is in the modules list
        if module_name not in translation.modules:
            translation.modules.append(module_name)

        # Add or update the module override
        translation.translations[locale].module_overrides[module_name] = text
        translation.translations[locale].updated_at = datetime.now(timezone.utc)
        translation.updated_at = datetime.now(timezone.utc)

        # Save changes
        await self.engine.save(translation)
        return translation

    async def get_translations_map(
        self, locale: str, module_name: str, skip: int = 0, limit: int = None
    ) -> Dict[str, str]:
        """
        Get a flat map of all translations for a module and locale,
        applying module-specific overrides.
        
        Args:
            locale: Locale code
            module_name: Module name
            
        Returns:
            Dictionary with translation keys and texts
        """
        translations = await self.get_multi(
            filters={"modules": module_name}, skip=skip, limit=limit
        )

        result = {}
        for translation in translations:
            if translation.translations and locale in translation.translations:
                result[translation.key] = translation.translations[locale].text
                if module_name in translation.translations[locale].module_overrides:
                    result[translation.key] = translation.translations[locale].module_overrides[module_name]
            else:
                result[translation.key] = translation.key

        return result

    async def delete_locale_translation(
        self, key: str, locale: str
    ) -> bool:
        """
        Remove a specific locale from a translation.
        """
        translation = await self.get_by_key(key=key)
        if not translation:
            return False

        if locale in translation.translations:
            del translation.translations[locale]
            translation.updated_at = datetime.now(timezone.utc)
            await self.engine.save(translation)
            return True

        return False


# Create a singleton instance
crud_translation = CRUDTranslation(Translation)
