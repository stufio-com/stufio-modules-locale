from fastapi import APIRouter

router = APIRouter()

# Include routes for locales and translations
from .locales import router as locales_router
from .translations import router as translations_router
from .admin_locales import router as admin_locales_router
from .admin_translations import router as admin_translations_router

from stufio.core.config import get_settings

settings = get_settings()

router.include_router(locales_router, prefix="/i18n", tags=["locales"])
router.include_router(translations_router, prefix="/i18n", tags=["translations"])

router.include_router(admin_locales_router, prefix=settings.API_ADMIN_STR + "/i18n", tags=["admin", "locales"])
router.include_router(admin_translations_router, prefix=settings.API_ADMIN_STR + "/i18n", tags=["admin", "translations"])
