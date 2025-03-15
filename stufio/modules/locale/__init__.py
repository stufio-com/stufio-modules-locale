from fastapi import FastAPI
from typing import List, Any, Tuple

from stufio.core.module_registry import ModuleInterface
from .api import api_router
from .models import Locale, Translation
from .middleware import LocaleMiddleware
from .__version__ import __version__
from .config import settings


class LocaleModule(ModuleInterface):
    """Locale and translation management module."""

    __version__ = __version__

    def register_routes(self, app: FastAPI, router_prefix: str = None) -> None:
        """Register this module's routes with the FastAPI app."""
        # Register routes
        app.include_router(api_router, prefix=router_prefix)

    def get_middlewares(self) -> List[Tuple]:
        """Return middleware classes for this module.

        Returns:
            List of (middleware_class, args, kwargs) tuples
        """
        return [(LocaleMiddleware, {}, {})]

    # For backwards compatibility
    def register(self, app: FastAPI) -> None:
        """Legacy registration method."""
        self.register_routes(app)
        # Don't add middleware here anymore

    def get_models(self) -> List[Any]:
        """Return this module's database models."""
        return [Locale, Translation]


# For backward compatibility
__all__ = ["api_router", "settings", "LocaleModule"]