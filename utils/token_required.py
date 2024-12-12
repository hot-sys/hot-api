from functools import wraps
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from utils.api_response import api_response

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        request = args[0]
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return api_response(message="Invalid token", success=False, status_code=401)

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, settings.TOKEN_KEY, algorithms=["HS256"])
            request.idUser = payload.get('id')
            request.idRole = payload.get('role')
            request.passwordVersion = payload.get('passwordVersion')
            if not request.idUser and request.idRole:
                return api_response(message="Invalid token", success=False, status_code=401)
        except jwt.ExpiredSignatureError:
            return api_response(message="Token has expired", success=False, status_code=401)
        except jwt.InvalidTokenError as e:
            return api_response(message=str(e), success=False, status_code=401)

        return f(*args, **kwargs)
    return decorated
