from datetime import datetime
from gc import collect
from typing import Optional
from odmantic import Model, Field, Index
from pydantic import ConfigDict


class Locale(Model):
    """MongoDB model for locales."""
    code: str = Field(description="The locale code, e.g., 'en-US'", index=True, unique=True)
    name: str = Field(description="The name of the language, e.g., 'English'")
    localized_name: str = Field(description="Name of language in native translation, e.g., 'English'")
    country: str = Field(default="", description="The name of the country, e.g., 'US'")
    details: Optional[str] = Field(default=None, description="Optional details about the locale")
    active: bool = Field(default=True, description="Whether this locale is active")
    sort_order: int = Field(default=0, description="Sort order (0 = alphabetical)")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(
        collection="i18n_locales",
        indexes=[
            Index("code", "country", unique=True),
            Index(
                "active",
                "code",
            ),
        ],
    )


class Translation(Model):
    """MongoDB model for translations."""
    key: str = Field(description="The key for the translation", index=True)
    locale: str = Field(
        description="The locale for the translation, e.g., 'en-US'", index=True
    )
    module_name: str = Field(
        description="The name of the module the translation belongs to", index=True
    )
    value: str = Field(description="The translated value")
    details: Optional[str] = Field(default=None, description="Optional details about the translation")
    discovered_at: Optional[datetime] = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(
        collection="i18n_translations",
        indexes=[
            Index("key", "locale", "module_name", unique=True),
            Index("key", "locale"),
        ]
    )
