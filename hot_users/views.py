from django.contrib.auth.hashers import check_password, make_password
from utils.token_required import token_required
from rest_framework.decorators import api_view, authentication_classes
from .models import User, Role
from .serializers import UserSerializer, UserSerializerResponse, RoleSerializer, LoginDTO, RegisterDTO, RoleDTO
from utils.api_response import api_response
from hot_users.decorators.checkUser import checkUser
from hot_users.decorators.checkAdmin import checkAdmin
import jwt
from django.conf import settings
from datetime import datetime, timedelta

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
                try:
                    dataRole = RoleSerializer(user.idRole)
                except Role.DoesNotExist:
                    return api_response(message="Role not found", success=False, status_code=404)
                access_payload = {
                    'id': user.idUser,
                    'role': dataRole.data["idRole"],
                    'passwordVersion': user.passwordVersion,
                    'exp': datetime.utcnow() + timedelta(minutes=15),
                    'iat': datetime.utcnow()
                }
                refresh_payload = {
                    'id': user.idUser,
                    'role': dataRole.data["idRole"],
                    'passwordVersion': user.passwordVersion,
                    'exp': datetime.utcnow() + timedelta(days=1),
                    'iat': datetime.utcnow()
                }
                access_token = jwt.encode(access_payload, settings.TOKEN_KEY, algorithm='HS256')
                refresh_token = jwt.encode(refresh_payload, settings.TOKEN_KEY, algorithm='HS256')
                return api_response(data={"access_token": access_token, "refresh_token": refresh_token}, message="Login successful")
        except User.DoesNotExist:
            pass

        return api_response(message="Invalid credentials", success=False, status_code=400)
    return api_response(data=dto.errors, message="Invalid input data", success=False, status_code=400)

@api_view(['POST'])
@authentication_classes([])
@token_required
@checkUser
@checkAdmin
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


@api_view(['GET'])
@authentication_classes([])
@token_required
@checkUser
def current_user(request):
    try:
        idUser = request.idUser
        user = User.objects.get(idUser=idUser)
        serializer = UserSerializerResponse(user)
        return api_response(data=serializer.data)
    except User.DoesNotExist:
        return api_response(message="User not found", success=False, status_code=404)


@api_view(['GET'])
@authentication_classes([])
@token_required
@checkUser
@checkAdmin
def get_all_users(request):
    try:
        users = User.objects.all()
        serializer = UserSerializerResponse(users, many=True)
        return api_response(data=serializer.data)
    except User.DoesNotExist:
        return api_response(message="Users not found", success=False, status_code=404)

@api_view(['GET'])
@authentication_classes([])
@token_required
@checkUser
def get_user(request, idUser):
    try:
        user = User.objects.get(id=idUser)
        serializer = UserSerializerResponse(user)
        return api_response(data=serializer.data)
    except User.DoesNotExist:
        return api_response(message="User not found", success=False, status_code=404)

@api_view(['GET'])
@authentication_classes([])
@token_required
@checkUser
@checkAdmin
def get_role(request, idRole):
    try:
        role = Role.objects.get(idRole=idRole)
        serializer = RoleSerializer(role)
        return api_response(data=serializer.data)
    except Role.DoesNotExist:
        return api_response(message="Role not found", success=False, status_code=404)

@api_view(['GET'])
@authentication_classes([])
@token_required
@checkUser
@checkAdmin
def get_all_roles(request):
    try:
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return api_response(data=serializer.data)
    except Role.DoesNotExist:
        return api_response(message="Roles not found", success=False, status_code=404)

@api_view(['POST'])
@authentication_classes([])
@token_required
@checkUser
@checkAdmin
def create_role(request):
    try:
        data = request.data
        dto = RoleDTO(data=data)
        if dto.is_valid():
            validated_data = dto.validated_data
            serializer = RoleSerializer(data=validated_data)
            if serializer.is_valid():
                serializer.save()
                return api_response(data=serializer.data, message="Role created successfully")
            return api_response(message="Invalid role already exist", success=False, status_code=400)
        return api_response(data=dto.errors, message="Invalid input data", success=False, status_code=400)
    except Role.DoesNotExist:
        return api_response(message="Role not found", success=False, status_code=404)