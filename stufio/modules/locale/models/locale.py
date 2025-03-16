from datetime import datetime
from typing import Optional
from odmantic import Model, Field, Index
from pydantic import ConfigDict

from stufio.db.mongo_base import MongoBase, datetime_now_sec


class Locale(MongoBase):
    """MongoDB model for locales."""
    code: str = Field(description="The locale code, e.g., 'en-US'", index=True, unique=True)
    name: str = Field(description="The name of the language, e.g., 'English'")
    localized_name: str = Field(description="Name of language in native translation, e.g., 'English'")
    country: str = Field(default="", description="The name of the country, e.g., 'US'")
    details: Optional[str] = Field(default=None, description="Optional details about the locale")
    active: bool = Field(default=True, description="Whether this locale is active")
    sort_order: int = Field(default=0, description="Sort order (0 = alphabetical)")
    created_at: datetime = Field(default_factory=datetime_now_sec)
    updated_at: datetime = Field(default_factory=datetime_now_sec)

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
