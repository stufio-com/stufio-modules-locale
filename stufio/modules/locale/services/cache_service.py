from redis import Redis
from typing import Any, Dict, Optional

class CacheService:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def get_translation(self, locale: str, key: str) -> Optional[str]:
        """Retrieve a translation from the cache by locale and key."""
        cache_key = f"translation:{locale}:{key}"
        return self.redis_client.get(cache_key)

    def set_translation(self, locale: str, key: str, value: str, expiration: int = 3600) -> None:
        """Set a translation in the cache with an expiration time."""
        cache_key = f"translation:{locale}:{key}"
        self.redis_client.set(cache_key, value, ex=expiration)

    def clear_translation(self, locale: str, key: str) -> None:
        """Clear a specific translation from the cache."""
        cache_key = f"translation:{locale}:{key}"
        self.redis_client.delete(cache_key)

    def clear_all_translations(self, locale: str) -> None:
        """Clear all translations for a specific locale from the cache."""
        keys = self.redis_client.keys(f"translation:{locale}:*")
        if keys:
            self.redis_client.delete(*keys)

cache_translations = CacheService(Redis())