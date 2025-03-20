from fastapi import APIRouter


from .locales import router as locales_router
from .translations import router as translations_router
from .internal_translations import router as internal_translations_router
from .admin_locales import router as admin_locales_router
from .admin_translations import router as admin_translations_router
from stufio.api.admin import admin_router, internal_router


router = APIRouter()

# Include routes for locales and translations
router.include_router(locales_router, prefix="/i18n", tags=["locales"])
router.include_router(translations_router, prefix="/i18n", tags=["translations"])

# Include internal routes for translations
internal_router.include_router(internal_translations_router, prefix="/i18n", tags=["translations"])

# Include admin routers
admin_router.include_router(admin_locales_router, prefix="/i18n", tags=["locales"])
admin_router.include_router(admin_translations_router, prefix="/i18n", tags=["translations"])
