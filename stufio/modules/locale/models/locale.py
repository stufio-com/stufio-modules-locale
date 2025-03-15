from datetime import datetime
from typing import Optional
from odmantic import Model, Field, EmbeddedModel


class Locale(Model):
    """MongoDB model for locales."""
    code: str = Field(description="The locale code, e.g., 'en-US'", index=True, unique=True)
    name: str = Field(description="The name of the language, e.g., 'English'")
    localized_name: str = Field(description="Name of language in native translation, e.g., 'English'")
    country: Optional[str] = Field(default=None, description="The name of the country, e.g., 'US'")
    details: Optional[str] = Field(default=None, description="Optional details about the locale")
    active: bool = Field(default=True, description="Whether this locale is active")
    sort_order: int = Field(default=0, description="Sort order (0 = alphabetical)")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        collection = "i18n_locales"


class Translation(Model):
    """MongoDB model for translations."""
    module_name: str = Field(description="The name of the module the translation belongs to", index=True)
    key: str = Field(description="The key for the translation", index=True)
    value: str = Field(description="The translated value")
    locale: str = Field(description="The locale for the translation, e.g., 'en-US'", index=True)
    details: Optional[str] = Field(default=None, description="Optional details about the translation")
    discovered_at: Optional[datetime] = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        collection = "i18n_translations"
        
    class Meta:
        indexes = [
            [("key", "locale", "module_name"), {"unique": True}]
        ]