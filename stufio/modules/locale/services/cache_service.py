from typing import Dict, Optional, List
from stufio.db.redis import RedisClient
from stufio.core.config import settings

class CacheService:
    """Service for caching translations using Redis."""
    
    async def get_translation(self, locale: str, key: str, module: Optional[str] = None) -> Optional[str]:
        """Retrieve a translation from the cache by locale and key."""
        redis = await RedisClient()
        # Use module-specific key if provided, otherwise use default
        cache_key = f"translation:{locale}:{key}:{module or 'default'}"
        return await redis.get(cache_key)
    
    async def set_translation(self, locale: str, key: str, value: str, module: Optional[str] = None, expiration: int = 3600) -> None:
        """Set a translation in the cache with an expiration time."""
        redis = await RedisClient()
        cache_key = f"translation:{locale}:{key}:{module or 'default'}"
        await redis.set(cache_key, value, ex=expiration)
    
    async def set_bulk_translations(self, locale: str, translations: Dict[str, str], module: Optional[str] = None, expiration: int = 3600) -> None:
        """Set multiple translations in the cache for a locale."""
        if not translations:
            return
            
        redis = await RedisClient()
        pipeline = redis._client.pipeline()  # Access underlying client for pipeline
        
        for key, value in translations.items():
            cache_key = f"translation:{locale}:{key}:{module or 'default'}"
            pipeline.set(cache_key, value, ex=expiration)
            
        await pipeline.execute()
    
    async def clear_translation(self, locale: str, key: str) -> None:
        """Clear all cached versions of a translation (all modules)."""
        redis = await RedisClient()
        pattern = f"translation:{locale}:{key}:*"
        
        async for key in redis._client.scan_iter(match=pattern):
            await redis.delete(key)
    
    async def clear_module_translations(self, locale: str, module: str) -> None:
        """Clear all translations for a specific locale and module."""
        redis = await RedisClient()
        pattern = f"translation:{locale}:*:{module}"
        
        keys = []
        async for key in redis._client.scan_iter(match=pattern):
            keys.append(key)
        
        # Delete in batches
        if keys:
            for i in range(0, len(keys), 1000):
                batch = keys[i:i+1000]
                if batch:
                    await redis._client.delete(*batch)
        
        # Also clear the translation map for this locale+module
        map_key = f"translations_map:{locale}:{module}"
        await redis.delete(map_key)
    
    async def clear_all_translations(self, locale: str) -> None:
        """Clear all translations for a specific locale from the cache."""
        redis = await RedisClient()
        pattern = f"translation:{locale}:*"
        
        # Collect keys to delete
        keys = []
        async for key in redis._client.scan_iter(match=pattern):
            keys.append(key)
        
        # Delete in batches
        if keys:
            for i in range(0, len(keys), 1000):
                batch = keys[i:i+1000]
                if batch:
                    await redis._client.delete(*batch)
        
        # Also delete any translation maps
        pattern = f"translations_map:{locale}:*"
        async for key in redis._client.scan_iter(match=pattern):
            await redis.delete(key)
    
    async def get_translations_for_module(self, locale: str, module: str) -> Dict[str, str]:
        """Get all translations for a specific locale and module from the cache."""
        redis = await RedisClient()
        
        # Check for the cached map first
        map_key = f"translations_map:{locale}:{module}"
        cached_map = await redis.get(map_key)
        if cached_map:
            try:
                import json
                return json.loads(cached_map)
            except:
                # If there's an error parsing the JSON, continue to individual keys
                pass
        
        # Fall back to individual keys
        pattern = f"translation:{locale}:*:{module}"
        result = {}
        
        # Collect translations for the module
        async for key in redis._client.scan_iter(match=pattern):
            # Format is "translation:{locale}:{key}:{module}"
            parts = key.split(":", 3)
            if len(parts) >= 3:
                original_key = parts[2]  # Get the translation key part
                value = await redis.get(key)
                if value:
                    result[original_key] = value
        
        # Also check default translations (may be used as fallback)
        pattern = f"translation:{locale}:*:default"
        async for key in redis._client.scan_iter(match=pattern):
            parts = key.split(":", 3)
            if len(parts) >= 3:
                original_key = parts[2]
                # Only add if not already in module-specific results
                if original_key not in result:
                    value = await redis.get(key)
                    if value:
                        result[original_key] = value
                
        return result
    
    async def set_translations_map(self, locale: str, module: str, translations_map: Dict[str, str], expiration: int = 300) -> None:
        """Cache a pre-built translations map for fast retrieval."""
        redis = await RedisClient()
        map_key = f"translations_map:{locale}:{module}"
        
        import json
        await redis.set(map_key, json.dumps(translations_map), ex=expiration)

# Create a singleton instance
cache_service = CacheService()

# Helper functions for clearing cache
async def cache_translations(locale: str) -> None:
    """Clear all translations cache for a specific locale."""
    await cache_service.clear_all_translations(locale)

async def cache_module_translations(locale: str, module: str) -> None:
    """Clear translations cache for a specific locale and module."""
    await cache_service.clear_module_translations(locale, module)
