from django.core.cache import cache
from django.conf import settings


# Set cache type
def setCache(request, cache_type, location=None, timeout=None, client_class=None):
    cache_backend = settings.CACHES.get(cache_type)

    if cache_backend:
        cache_obj = cache.get_cache(cache_backend['BACKEND'])
        # Use the cache_obj for caching operations

        if location:
            cache_obj.set_location(location)

        if timeout:
            cache_obj.set_timeout(timeout)

        if client_class:
            cache_obj.set_client_class(client_class)
    else:
        # Handle unsupported cache type
        pass


# Low-Level Cache API: Django's caching framework also provides a low-level
# cache API that allows you to cache arbitrary data or function results.

# Get cashed data or from DB
def getFromCacheOrDb(model, dataKey):
    # Check if the data is available in the cache
    # dataKey = 'my_data_key'
    data = cache.get(dataKey)
    if data is not None:
        return data

    # If data is not in the cache, fetch it from the database
    queryset = model.objects.all()
    # Perform any necessary filtering or ordering on the queryset

    # Convert the queryset to a list or serialize it as per your needs
    data = list(queryset)

    # Store the fetched data in the cache for future use
    # dataKey = 'my_data_key'
    cache.set(dataKey, data, 3600)  # Cache the data for 1 hour

    return data
