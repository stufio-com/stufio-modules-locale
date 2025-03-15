from pydantic import BaseModel, Field
from typing import Optional

class Translation(BaseModel):
    module_name: str = Field(..., description="The name of the module the translation belongs to.")
    key: str = Field(..., description="The key for the translation.")
    value: str = Field(..., description="The translated value.")
    locale: str = Field(..., description="The locale code (e.g., 'en', 'fr', 'es').")
    details: Optional[str] = Field(None, description="Optional details about the translation.")

    class Config:
        schema_extra = {
            "example": {
                "module_name": "user_module",
                "key": "welcome_message",
                "value": "Welcome to our application!",
                "locale": "en",
                "details": "Displayed on the homepage."
            }
        }