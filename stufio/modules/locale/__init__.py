from fastapi import FastAPI
from typing import List, Any, Tuple

from stufio.core.module_registry import ModuleInterface
from .middleware import LocaleMiddleware
from .__version__ import __version__
from .config import LocaleSettings
from .settings import settings_registry


class LocaleModule(ModuleInterface):
    """Locale and translation management module."""

    version = __version__

    def register_routes(self, app: FastAPI) -> None:
        """Register this module's routes with the FastAPI app."""
        from .api import router as api_router
        # Register routes
        app.include_router(api_router, prefix=self.routes_prefix)

    def get_middlewares(self) -> List[Tuple]:
        """Return middleware classes for this module.

        Returns:
            List of (middleware_class, args, kwargs) tuples
        """
        return [(LocaleMiddleware, {}, {})]  # Fix: use empty list for args


# For backward compatibility
__all__ = ["__version__", "LocaleSettings", "LocaleModule"]
