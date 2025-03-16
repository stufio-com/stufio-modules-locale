from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any


class TranslationBase(BaseModel):
    """Base schema for translations with shared attributes."""
    locale: str = Field(
        ..., 
        description="The locale code for the translation, e.g., 'en'",
        examples=["en", "fr", "es"]
    )
    key: str = Field(
        ..., 
        description="The key for the translation, usually in dot notation",
        examples=["common.welcome", "errors.not_found"]
    )
    value: str = Field(
        ..., 
        description="The translated value",
        examples=["Welcome to our app", "Page not found"]
    )
    module_name: str = Field(
        ..., 
        description="The name of the module the translation belongs to",
        examples=["core", "auth", "products"]
    )
    details: Optional[str] = Field(
        None, 
        description="Optional details about the translation or context"
    )


class TranslationCreate(TranslationBase):
    """Schema for creating a new translation."""
    discovered_at: Optional[datetime] = Field(
        None,
        description="When this translation key was first discovered (auto-populated if None)"
    )


class TranslationUpdate(BaseModel):
    """Schema for updating an existing translation."""
    value: Optional[str] = Field(None, description="The translated value")
    details: Optional[str] = Field(None, description="Optional details about the translation")
    active: Optional[bool] = Field(None, description="Whether this translation is active")


class TranslationInDB(TranslationBase):
    """Schema for translation responses that include database fields."""
    id: str = Field(..., description="The translation ID")
    discovered_at: Optional[datetime] = Field(None, description="When this translation was first discovered")
    created_at: datetime = Field(..., description="When this translation was created")
    updated_at: datetime = Field(..., description="When this translation was last updated")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "60d21b4967d0d8992e610c85",
                "locale": "en",
                "key": "common.welcome",
                "value": "Welcome to our application",
                "module_name": "core",
                "details": "Shown on the homepage after login",
                "discovered_at": "2025-03-15T10:00:00Z",
                "created_at": "2025-03-15T10:30:00Z",
                "updated_at": "2025-03-16T14:45:00Z"
            }
        }
    )


# For backward compatibility
class Translation(TranslationInDB):
    pass


class TranslationResponse(TranslationInDB):
    """Schema for translation responses in the API."""
    pass


class TranslationBulkImport(BaseModel):
    """Schema for bulk importing multiple translations."""
    translations: list[TranslationCreate] = Field(..., description="List of translations to import")
    overwrite_existing: bool = Field(False, description="Whether to overwrite existing translations")


class TranslationBulkExport(BaseModel):
    """Schema for exported translations, grouped by locale."""
    locale: str = Field(..., description="The locale code")
    translations: Dict[str, str] = Field(..., description="Key-value pairs of translations")
