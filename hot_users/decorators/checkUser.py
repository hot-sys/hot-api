from functools import wraps
from hot_users.models import User, Role
from hot_users.serializers import RoleSerializer
from utils.api_response import api_response

def checkUser(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        request = args[0]
        idUser = request.idUser
        idRole = request.idRole
        passwordVersion = request.passwordVersion
        try:
            user = User.objects.get(idUser=idUser)
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