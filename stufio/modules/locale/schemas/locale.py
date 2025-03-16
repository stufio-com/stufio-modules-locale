from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from odmantic import ObjectId

# Locale schemas
class LocaleBase(BaseModel):
    """Base schema for locales with shared attributes."""
    code: str = Field(..., description="The locale code, e.g., 'en'")
    name: str = Field(..., description="The name of the language, e.g., 'English'")
    localized_name: str = Field(..., description="Name of language in native translation, e.g., 'English'")
    country: Optional[str] = Field(None, description="The name of the country, e.g., 'US'")
    details: Optional[str] = Field(None, description="Optional details about the locale")
    active: bool = Field(True, description="Whether this locale is active")
    sort_order: int = Field(0, description="Sort order (0 = alphabetical)")


class LocaleCreate(LocaleBase):
    """Schema for creating a new locale."""
    pass


class LocaleUpdate(BaseModel):
    """Schema for updating an existing locale."""
    code: Optional[str] = Field(None, description="The locale code, e.g., 'en'")
    name: Optional[str] = Field(None, description="The name of the language, e.g., 'English'")
    localized_name: Optional[str] = Field(None, description="Name of language in native translation")
    country: Optional[str] = Field(None, description="The name of the country, e.g., 'US'")
    details: Optional[str] = Field(None, description="Optional details about the locale")
    active: Optional[bool] = Field(None, description="Whether this locale is active")
    sort_order: Optional[int] = Field(None, description="Sort order (0 = alphabetical)")


class LocaleInDB(LocaleBase):
    """Schema for locale responses that include database fields."""
    id: Optional[ObjectId] = Field(None, description="The locale ID")
    created_at: Optional[datetime] = Field(None, description="When this locale was created")
    updated_at: Optional[datetime] = Field(None, description="When this locale was last updated")

    class Config:
        from_attributes = True


class LocaleResponse(LocaleInDB):
    """Schema for locale responses."""
    pass
