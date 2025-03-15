from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class TranslationBase(BaseModel):
    """Base schema for translations with shared attributes."""
    locale: str = Field(..., description="The locale for the translation, e.g., 'en'")
    key: str = Field(..., description="The key for the translation")
    value: str = Field(..., description="The translated value")
    module_name: str = Field(..., description="The name of the module the translation belongs to")
    details: Optional[str] = Field(None, description="Optional details about the translation")


class TranslationCreate(TranslationBase):
    """Schema for creating a new translation."""
    pass


class TranslationUpdate(BaseModel):
    """Schema for updating an existing translation."""
    value: Optional[str] = Field(None, description="The translated value")
    details: Optional[str] = Field(None, description="Optional details about the translation")


class TranslationInDB(TranslationBase):
    """Schema for translation responses that include database fields."""
    id: str = Field(..., description="The translation ID")
    discovered_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# For backward compatibility
class Translation(TranslationInDB):
    pass


class TranslationResponse(TranslationInDB):
    """Schema for translation responses."""
    pass
