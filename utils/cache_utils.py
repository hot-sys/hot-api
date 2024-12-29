import logging
from django.core.cache import cache
import hashlib
logger = logging.getLogger(__name__)

def generate_cache_key(base_key, **kwargs):
    raw_key = base_key + "_" + "_".join(f"{k}={v}" for k, v in kwargs.items())
    hashed_key = hashlib.md5(raw_key.encode('utf-8')).hexdigest()

    tracked_keys = cache.get('tracked_keys', {})
    tracked_keys[raw_key] = hashed_key
    cache.set('tracked_keys', tracked_keys)

    return hashed_key

def list_cached_keys_by_prefix(prefix):
    tracked_keys = cache.get('tracked_keys', {})
    matching_keys = {raw_key: hashed_key for raw_key, hashed_key in tracked_keys.items() if raw_key.startswith(prefix)}
    return matching_keys

def get_cached_data(cache_key):
    return cache.get(cache_key)

def set_cached_data(key, value, timeout=None):
    logger.info(f"Setting cache for key: {key}")
    cache.set(key, value, timeout)

def get_cached_data(key):
    logger.info(f"Getting cache for key: {key}")
    return cache.get(key)

def delete_cached_data(key):
    logger.info(f"Deleting cache for key: {key}")
    cache.delete(key)

def delete_cache_by_prefix(prefix):
    tracked_keys = cache.get('tracked_keys', {})

    keys_to_delete = [hashed_key for raw_key, hashed_key in tracked_keys.items() if raw_key.startswith(prefix)]

    for hashed_key in keys_to_delete:
        logger.info(f"Deleting cache for key: {hashed_key}")
        cache.delete(hashed_key)

    updated_keys = {raw_key: hashed_key for raw_key, hashed_key in tracked_keys.items() if raw_key not in keys_to_delete}
    cache.set('tracked_keys', updated_keys)
