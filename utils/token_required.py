import jwt
from rest_framework import status
from functools import wraps
from django.conf import settings
from .api_response import api_response

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        request = args[0]
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return api_response(message="Token is missing or invalid", success=False, status_code=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print(payload)
            request.idUser = payload.get('id')
            if not request.idUser:
                raise jwt.InvalidTokenError("Token has no user ID")
        except jwt.ExpiredSignatureError:
            return api_response(message="Token has expired", success=False, status_code=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError as e:
            return api_response(message=str(e), success=False, status_code=status.HTTP_401_UNAUTHORIZED)

        return f(*args, **kwargs)
    return decorated