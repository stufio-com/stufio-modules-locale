from pydantic import BaseModel
from pymongo import settings
from stufio.core.config import ModuleSettings, get_settings

settings = get_settings()

class LocaleSettings(ModuleSettings, BaseModel):
    DEFAULT_LOCALE: str = "en"
    SUPPORTED_LOCALES: list[str] = ["en", "fr", "es", "de", "pl", "ru", "pt", "it", "nl", "dk", "ua", "ro", "cz", "se", "no", "fi", "gr", "tr", "hu", "bg", "sk", "hr", "lt", "lv", "ee"]
    FALLBACK_LOCALE: str = "en"
    USE_FALLBACK: bool = True


# Register these settings with the core
settings.register_module_settings("locale", LocaleSettings)
