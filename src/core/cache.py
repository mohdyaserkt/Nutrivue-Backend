from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from typing import Optional, Any
from fastapi import UploadFile
import hashlib

async def init_cache():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="food-cache")

def image_cache_key_builder(
    func: Any,
    namespace: Optional[str] = "",
    *,
    request: Optional[Any] = None,
    file: UploadFile = None,
    **kwargs: Any
) -> str:
    """Build cache key from file content hash"""
    if file is None:
        raise ValueError("File is required for cache key generation")
    
    # Read first 1MB for hash (adjust size as needed)
    file.file.seek(0)
    file_content = file.file.read(1024 * 1024)
    file.file.seek(0)
    
    # Generate SHA256 hash of file content
    file_hash = hashlib.sha256(file_content).hexdigest()
    return f"{namespace}::{func.__module__}.{func.__name__}::{file_hash}"