from django.contrib.auth.hashers import check_password, make_password
from rest_framework.decorators import api_view
from .models import User, Role
from .serializers import UserSerializer, RoleSerializer, LoginDTO, RegisterDTO
from utils.api_response import api_response
from utils.token_required import token_required
import jwt
from django.conf import settings
from datetime import datetime, timedelta

@api_view(['POST'])
def create(request):
    data = request.data
    dto = RegisterDTO(data=data)
    if dto.is_valid():
        validated_data = dto.validated_data
        validated_data['password'] = make_password(validated_data['password'])
        serializer = UserSerializer(data=validated_data)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, message="User registered successfully")
        return api_response(data=serializer.errors, message="Invalid user data", success=False, status_code=400)
    return api_response(data=dto.errors, message="Invalid input data", success=False, status_code=400)

@api_view(['POST'])
def login(request):
    data = request.data
    dto = LoginDTO(data=data)
    if dto.is_valid():
        validated_data = dto.validated_data
        login = validated_data['login']
        password = validated_data['password']

        try:
            user = User.objects.get(login=login)
            if check_password(password, user.password):
                payload = {
                    'id': user.idUser,
                    'exp': datetime.utcnow() + timedelta(minutes=1),
                    'iat': datetime.utcnow()
                }
                print(payload)
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                return api_response(data={"token": token}, message="Login successful")
        except User.DoesNotExist:
            pass

        return api_response(message="Invalid credentials", success=False, status_code=400)
    return api_response(data=dto.errors, message="Invalid input data", success=False, status_code=400)

@api_view(['GET'])
def current_user(request):
    try:
        idUser = 1
        user = User.objects.get(idUser=idUser)
        serializer = UserSerializer(user)
        return api_response(data=serializer.data)
    except User.DoesNotExist:
        return api_response(message="User not found", success=False, status_code=404)


@api_view(['GET'])
def get_all_users(request):
    try:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return api_response(data=serializer.data)
    except User.DoesNotExist:
        return api_response(message="Users not found", success=False, status_code=404)

@api_view(['GET'])
def get_user(request, idUser):
    try:
        user = User.objects.get(id=idUser)
        serializer = UserSerializer(user)
        return api_response(data=serializer.data)
    except User.DoesNotExist:
        return api_response(message="User not found", success=False, status_code=404)

@api_view(['GET'])
def get_role(request, idRole):
    try:
        role = Role.objects.get(idRole=idRole)
        serializer = RoleSerializer(role)
        return api_response(data=serializer.data)
    except Role.DoesNotExist:
        return api_response(message="Role not found", success=False, status_code=404)

@api_view(['GET'])
def get_all_roles(request):
    try:
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return api_response(data=serializer.data)
    except Role.DoesNotExist:
        return api_response(message="Roles not found", success=False, status_code=404)