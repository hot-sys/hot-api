from functools import wraps
from utils.api_response import api_response

def checkAdmin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        request = args[0]
        if request.idRole != 1:
            return api_response(message="Unauthorized access", success=False, status_code=401)
        return f(*args, **kwargs)
    return decorated