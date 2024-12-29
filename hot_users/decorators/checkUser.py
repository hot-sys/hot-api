from functools import wraps
from hot_users.models import User, Role
from hot_users.serializers import RoleSerializer
from utils.api_response import api_response
from utils.cache_utils import generate_cache_key, get_cached_data, set_cached_data, delete_cache_by_prefix, list_cached_keys_by_prefix
from django.conf import settings

def checkUser(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        request = args[0]
        idUser = request.idUser
        idRole = request.idRole
        passwordVersion = request.passwordVersion
        try:
            cache_key = generate_cache_key('user-check', idUser=idUser, idRole=idRole, passwordVersion=passwordVersion)
            cached_data = get_cached_data(cache_key)
            if cached_data:
                user = cached_data
            else:
                user = User.objects.get(idUser=idUser)
                set_cached_data(cache_key, user, settings.CACHE_TTL)
            try:
                dataRole = RoleSerializer(user.idRole)
            except Role.DoesNotExist:
                return api_response(message="Role not found", success=False, status_code=404)
            if dataRole.data["idRole"] != idRole or user.passwordVersion != passwordVersion:
                return api_response(message="Unauthorized access", success=False, status_code=401)
            request.userInstance = user
            return f(*args, **kwargs)
        except User.DoesNotExist:
            return api_response(message="Users not found", success=False, status_code=404)
    return decorated