from datetime import datetime
from typing import Optional
from odmantic import Model, Field, Index
from pydantic import ConfigDict


class Translation(Model):
    """MongoDB model for translations."""
    key: str = Field(description="The key for the translation", index=True)
    locale: str = Field(description="The locale for the translation, e.g., 'en-US'", index=True)
    module_name: str = Field(
        default="",
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
