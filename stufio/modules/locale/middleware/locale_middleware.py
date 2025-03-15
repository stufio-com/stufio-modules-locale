from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class LocaleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Extract locale from request headers or query parameters
        locale = request.headers.get("Accept-Language") or request.query_params.get("locale", "en")

        # Store the locale in the request state for later use
        request.state.locale = locale

        # Call the next middleware or endpoint
        response: Response = await call_next(request)

        return response
