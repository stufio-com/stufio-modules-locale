from datetime import datetime
from typing import Dict, Optional, List
from odmantic import Field, Index, EmbeddedModel
from pydantic import ConfigDict

from stufio.db.mongo_base import MongoBase, datetime_now_sec


class LocaleTranslation(EmbeddedModel):
    """Embedded model for a translation in a specific locale."""
    text: str = Field(description="The translated text")
    module_overrides: Dict[str, str] = Field(
        default_factory=dict,
        description="Module-specific overrides of this translation"
    )
    description: Optional[str] = Field(default=None, description="Optional description of this translation key")
    created_at: datetime = Field(default_factory=datetime_now_sec)
    updated_at: datetime = Field(default_factory=datetime_now_sec)


class Translation(MongoBase):
    """MongoDB model for translations with embedded locale translations."""
    key: str = Field(description="The translation key", index=True)
    modules: List[str] = Field(
        default_factory=list, 
        description="Additional modules this translation applies to (when shared)"
    )
    description: Optional[str] = Field(default=None, description="Optional description of this translation key")
    translations: Dict[str, LocaleTranslation] = Field(
        default_factory=dict, 
        description="Dictionary of translations where key is locale code and value is the translation"
    )
    created_at: datetime = Field(default_factory=datetime_now_sec)
    updated_at: datetime = Field(default_factory=datetime_now_sec)

    model_config = ConfigDict(
        collection="i18n_translations",
        indexes=[
            Index("key", unique=True),
        ],
    )
