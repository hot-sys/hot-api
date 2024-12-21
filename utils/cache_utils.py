from django.core.cache import cache
from django.views.decorators.cache import cache_page
from functools import wraps
from django.http import JsonResponse

def cache_response(timeout=60 * 15, cache_key_func=None):
    """
    Décorateur pour mettre en cache les réponses des endpoints.

    Args:
        timeout (int): Durée de vie du cache en secondes (par défaut : 15 minutes).
        cache_key_func (callable): Fonction pour générer une clé de cache unique.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            idUser = getattr(request, 'idUser', 'anonymous')  # Vérifier que 'idUser' est bien défini
            print(f"User ID: {idUser}") 
            
            # Générer la clé de cache en fonction de l'utilisateur ou du contexte
            if cache_key_func:
                key = cache_key_func(request, *args, **kwargs)
            else:
                idUser = getattr(request, 'idUser', 'anonymous')
                key = f"{request.path}:{idUser}"
            print('CACHEEEEEEEEEEEEEEEEEEEEEEEEE', key)
            # Appliquer le cache_page si la clé de cache est générée
            cached_view = cache_page(timeout)(view_func)

            # Vérifier si une réponse est déjà dans le cache
            cached_response = cache.get(key)
            if cached_response:
                print(f"Cache recup: {key}")
                return JsonResponse(cached_response, safe=False)

            # Exécuter la vue et mettre la réponse en cache
            response = cached_view(request, *args, **kwargs)

            # Si la réponse est un JsonResponse, la mettre en cache
            if isinstance(response, JsonResponse):
                try:
                    cache.set(key, response.content, timeout)
                    print(f"Cache set: {key}")
                except Exception as e:
                    print(f"Error caching response: {e}")

            return response
        return wrapped_view
    return decorator

def invalidate_user_cache(idUser):
    key = f"user:{idUser}:/current_user"
    cache.delete(key)