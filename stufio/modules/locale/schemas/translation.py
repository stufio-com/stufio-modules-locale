from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from odmantic import ObjectId


class LocaleTranslationBase(BaseModel):
    """Base schema for locale translations with shared attributes."""
    text: str = Field(..., description="The translated text")
    module_overrides: Optional[Dict[str, str]] = Field(
        default_factory=dict,
        description="Module-specific overrides of this translation"
    )
    description: Optional[str] = Field(None, description="Optional description for this locale translation")


class LocaleTranslationCreate(LocaleTranslationBase):
    """Schema for creating a new locale translation."""
    pass


class LocaleTranslationUpdate(BaseModel):
    """Schema for updating an existing locale translation."""
    text: Optional[str] = None
    module_overrides: Optional[Dict[str, str]] = None
    description: Optional[str] = None


class LocaleTranslationInDB(LocaleTranslationBase):
    """Schema for locale translation responses that include database fields."""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TranslationBase(BaseModel):
    """Base schema for translations with shared attributes."""
    key: str = Field(..., description="The translation key")
    modules: List[str] = Field(
        ..., description="Modules this translation applies to"
    )
    description: Optional[str] = Field(None, description="Optional description of this translation key")


class TranslationCreate(TranslationBase):
    """Schema for creating a new translation."""
    translations: Dict[str, LocaleTranslationCreate] = Field(default_factory=dict)


class TranslationUpdate(BaseModel):
    """Schema for updating an existing translation."""
    modules: Optional[List[str]] = None
    description: Optional[str] = None
    translations: Optional[Dict[str, LocaleTranslationUpdate]] = None


class TranslationInDB(TranslationBase):
    """Schema for translation responses that include database fields."""
    id: Optional[ObjectId] = None
    translations: Dict[str, LocaleTranslationInDB] = Field(default_factory=dict)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TranslationResponse(TranslationInDB):
    """Schema for translation responses."""
    pass


class ModuleOverrideUpdate(BaseModel):
    """Schema for updating a module-specific translation."""
    text: str = Field(..., description="The module-specific translation text")
    module: str = Field(..., description="The module name for this override")
