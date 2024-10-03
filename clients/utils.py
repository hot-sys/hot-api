import jwt
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from .serializers import UserClientSerializerReturn, UserClientRegisterSerializer, UserClientSerializer
from .models import UserClient
from functools import wraps

def generate_token(user):
    token = jwt.encode({
        'user': user,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, settings.TOKEN_KEY, algorithm='HS256')

    return token.decode('utf-8')

def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({'message': 'Entete vide'}, status=401)
        try:
            payload = jwt.decode(token, settings.TOKEN_KEY, algorithms=['HS256'])
            if 'user' in payload:
                try:
                    user = get_object_or_404(UserClient, id=int(payload['user']))
                    serializer = UserClientSerializerReturn(user)
                    request.user_actif = serializer.data
                    request.user_object = user
                except UserClient.DoesNotExist:
                    return JsonResponse({"message": "User not found"}, status=400)
            else:
                return JsonResponse({'message': 'Token invalide'}, status=401)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Token expiré'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'Token invalide'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper
