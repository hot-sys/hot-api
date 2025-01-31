from django.contrib.auth.hashers import check_password, make_password
from utils.token_required import token_required
from rest_framework.decorators import api_view, authentication_classes, parser_classes
from .models import User, Role
from .serializers import CreateUserSerializer, UserSerializerResponse, RoleSerializer, LoginDTO, RegisterDTO, UpdateUserDto, RoleDTO, UpdatePosteDTO
from utils.api_response import api_response
from hot_users.decorators.checkUser import checkUser
from hot_users.decorators.checkAdmin import checkAdmin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from utils.services.supabase_user_service import upload_images, remove_file
from utils.cache_utils import generate_cache_key, get_cached_data, set_cached_data, delete_cache_by_prefix, list_cached_keys_by_prefix
from django.conf import settings

@extend_schema(
    request=LoginDTO,
    responses={
        200: OpenApiResponse(description='Login successful'),
        400: OpenApiResponse(description='Invalid credentials'),
        404: OpenApiResponse(description='Role not found')
    },
    description="User login to obtain JWT tokens (access & refresh)",
    summary="User login",
)
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
                if dataRole.data["poste"] == "Room":
                    access_user = False
                else:
                    access_user = True
                datalogged = {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    'role': dataRole.data["idRole"],
                    'access_user': access_user,
                }
                return api_response(data=datalogged, message="Login successful", success=True, status_code=200)
        except User.DoesNotExist:
            return api_response(message="User not found", success=False, status_code=404)
        return api_response(message="Invalid credentials", success=False, status_code=400)
    return api_response(data=dto.errors, message="Invalid input data", success=False, status_code=400)

@extend_schema(
    request=RegisterDTO,
    responses={
        201: CreateUserSerializer,
        400: OpenApiResponse(description='Invalid input data or user data')
    },
    description="Endpoint to create a new user. The user must provide the necessary registration data.",
    summary="Create new user",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        )
    ]
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
@checkAdmin
def create(request):
    data = request.data
    dto = RegisterDTO(data=data)
    if dto.is_valid():
        validated_data = dto.validated_data
        validated_data['password'] = make_password(validated_data['password'])
        serializer = CreateUserSerializer(data=validated_data)
        if serializer.is_valid():
            serializer.save()
            delete_cache_by_prefix('users-')
            return api_response(data=serializer.data, message="User registered successfully", success=True, status_code=201)
        return api_response(data=serializer.errors, message="Invalid user data", success=False, status_code=400)
    return api_response(data=dto.errors, message="Invalid input data", success=False, status_code=400)

@extend_schema(
    request=UpdateUserDto,
    responses={
        200: UserSerializerResponse,
        400: OpenApiResponse(description='Invalid input data'),
        404: OpenApiResponse(description='User not found')
    },
    description="Endpoint to update profile picture of the current logged-in user. Requires user validation.",
    summary="Update profile picture of the current",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        )
    ]
)
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@parser_classes([MultiPartParser, FormParser])
@token_required
@checkUser
def upload_current(request):
    idUser = request.idUser
    try:
        user = User.objects.get(idUser=idUser)
        try:
            if user.image:
                remove_file(user.image)
        except Exception as e:
            pass
        files = request.FILES.getlist('image')
        if not files:
            return api_response(data=None, message="No images uploaded", success=False, status_code=400)
        urls = upload_images(files)
        for url in urls:
            user.image = url
            user.save()
        delete_cache_by_prefix('users-')
        return api_response(data=urls, message="Images uploaded successfully", success=True, status_code=200)
    except User.DoesNotExist:
        return api_response(data=None, message="User not found", success=False, status_code=404)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

@extend_schema(
    request="password",
    responses={
        200: OpenApiResponse(description='Current password is valid'),
        400: OpenApiResponse(description='Current password is required'),
        404: OpenApiResponse(description='User not found'),
        409: OpenApiResponse(description='Invalid current password')
    },
    description="Endpoint to check if the current password provided by the user is valid. Requires password.",
    summary="Check current password",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        )
    ]
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
def checkCurrentPass(request):
    data = request.data
    if 'currentPassword' not in data:
        return api_response(message="Current password is required", success=False, status_code=400)
    current_password = data['currentPassword']
    idUser = request.idUser
    try:
        user = User.objects.get(idUser=idUser)
        if not check_password(current_password, user.password):
            return api_response(message="Invalid current password", success=False, status_code=409)
        return api_response(message="Current password is valid", success=True, status_code=200)
    except User.DoesNotExist:
        return api_response(message="User not found", success=False, status_code=404)

@extend_schema(
    request=UpdateUserDto,
    responses={
        200: UserSerializerResponse,
        400: OpenApiResponse(description='Invalid input data'),
        404: OpenApiResponse(description='User not found')
    },
    description="Endpoint to update the details of the current logged-in user. Requires user validation.",
    summary="Update user details",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        )
    ]
)
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
def update_current_user(request):
    data = request.data
    dto = UpdateUserDto(data=data)
    if dto.is_valid():
        validated_data = dto.validated_data
        idUser = request.idUser
        try:
            user = User.objects.get(idUser=idUser)
            for key, value in validated_data.items():
                if key == 'password':
                    value = make_password(value)
                    user.passwordVersion += 1
                setattr(user, key, value)
            user.save()
            serializer = UserSerializerResponse(user)
            delete_cache_by_prefix('users-')
            return api_response(data=serializer.data, message="User updated successfully", success=True, status_code=200)
        except User.DoesNotExist:
            return api_response(message="User not found", success=False, status_code=404)
    return api_response(data=dto.errors, message="Invalid input data", success=False, status_code=400)

@extend_schema(
    request=UpdateUserDto,
    responses={
        200: UserSerializerResponse,
        400: OpenApiResponse(description='Invalid input data'),
        403: OpenApiResponse(description='Update other account available'),
        404: OpenApiResponse(description='User not found')
    },
    description="Endpoint to update the details of a user by Administration. Requires user validation and the ability (admin) to update other users.",
    summary="Update user details by admin",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idUser',
            required=True,
            type=int,
            location=OpenApiParameter.PATH
        )
    ]
)
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
@checkAdmin
def update_admin_user(request, idUser):
    data = request.data
    dto = UpdateUserDto(data=data)
    current_user = request.idUser
    if current_user == idUser:
        return api_response(message="Update other account available", success=False, status_code=403)
    if dto.is_valid():
        validated_data = dto.validated_data
        try:
            user = User.objects.get(idUser=idUser)
            for key, value in validated_data.items():
                if key == 'password':
                    value = make_password(value)
                    user.passwordVersion += 1
                setattr(user, key, value)
            user.save()
            serializer = UserSerializerResponse(user)
            delete_cache_by_prefix('users-')
            return api_response(data=serializer.data, message="User updated successfully", success=True, status_code=200)
        except User.DoesNotExist:
            return api_response(message="User not found", success=False, status_code=404)
    return api_response(data=dto.errors, message="Invalid input data", success=False, status_code=400)

@extend_schema(
    responses={
        200: UserSerializerResponse,
        400: OpenApiResponse(description='User already have this poste'),
        403: OpenApiResponse(description='Cannot update current user poste'),
        404: OpenApiResponse(description='Role or User not found')
    },
    description="Endpoint to update the poste of a user by Administration. Requires user validation and the ability (admin) to update other users.",
    summary="Update user poste by admin",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idUser',
            required=True,
            type=int,
            location=OpenApiParameter.PATH
        )
    ]
)
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
@checkAdmin
def update_poste(request, idUser):
    data = request.data
    current_user = request.idUser
    if current_user == idUser:
        return api_response(message="Cannot update current user poste", success=False, status_code=403)
    try:
        dto = UpdatePosteDTO(data=request.data)
        if dto.is_valid():
            user = User.objects.get(idUser=idUser)
            if data["idRole"] == UserSerializerResponse(user).data["idRole"]:
                return api_response(message="User already have this poste", success=False, status_code=400)
            user.idRole = dto.validated_data["idRole"]
            user.save()
            serializer = UserSerializerResponse(user)
            delete_cache_by_prefix('users-')
            return api_response(data=serializer.data, message="User poste updated successfully", success=True, status_code=200)
        return api_response(data=dto.errors, message="Invalid input data", success=False, status_code=400)
    except User.DoesNotExist:
        return api_response(message="User not found", success=False, status_code=404)

@extend_schema(
    responses={
        200: OpenApiResponse(description='User deleted successfully'),
        404: OpenApiResponse(description='User not found')
    },
    description="Endpoint to delete an user. Requires user validation and the ability (admin) to delete other users.",
    summary="Delete user by admin",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idUser',
            required=True,
            type=int,
            location=OpenApiParameter.PATH
        )
    ]
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
@checkAdmin
def delete_user(request, idUser):
    currentUser = request.idUser
    if currentUser == idUser:
        return api_response(message="Cannot delete current user account", success=False, status_code=403)
    try:
        user = User.objects.get(idUser=idUser)
        user.deletedAt = datetime.now()
        user.save()
        delete_cache_by_prefix('users-')
        return api_response(message="User deleted successfully", success=True, status_code=200)
    except User.DoesNotExist:
        return api_response(message="User not found", success=False, status_code=404)


@extend_schema(
    responses={
        200: OpenApiResponse(description='User recovered successfully'),
        404: OpenApiResponse(description='User not found')
    },
    description="Endpoint to recover a deleted user. Requires user validation and the ability (admin) to recover other users.",
    summary="Recover user by admin",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idUser',
            required=True,
            type=int,
            location=OpenApiParameter.PATH
        )
    ]
)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
@checkAdmin
def recover_user(request, idUser):
    try:
        current_user = request.idUser
        if current_user == idUser:
            return api_response(message="Cannot recover current user account", success=False, status_code=403)
        user = User.all_objects.get(idUser=idUser)
        if user.deletedAt == None:
            return api_response(message="User already active", success=False, status_code=400)
        user.deletedAt = None
        user.save()
        delete_cache_by_prefix('users-')
        return api_response(message="User recovered successfully", success=True, status_code=200)
    except User.DoesNotExist:
        return api_response(message="User not found", success=False, status_code=404)

@extend_schema(
    responses={
        200: UserSerializerResponse,
        404: OpenApiResponse(description='User not found')
    },
    description="Endpoint to fetch details of the current logged-in user",
    summary="Get current user details",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        )
    ]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
def current_user(request):
    try:
        idUser = request.idUser
        cache_key = generate_cache_key('users-current', idUser=idUser)
        cached_data = get_cached_data(cache_key)
        if cached_data:
            return api_response(data=cached_data, success=True, status_code=200)
        user = User.objects.get(idUser=idUser)
        serializer = UserSerializerResponse(user)
        set_cached_data(cache_key, serializer.data, settings.CACHE_TTL)
        return api_response(data=serializer.data, success=True, status_code=200)
    except User.DoesNotExist:
        return api_response(message="User not found", success=False, status_code=404)

@extend_schema(
    responses={
        200: UserSerializerResponse(many=True),
        404: OpenApiResponse(description='Users not found')
    },
    description="Endpoint to get all registered users. Requires admin privileges.",
    summary="Get all users",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        )
    ]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
@checkAdmin
def get_all_users(request):
    try:
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        cache_key = generate_cache_key('users-all', page=page, limit=limit)
        cached_data = get_cached_data(cache_key)
        if cached_data:
            return api_response(data=cached_data, success=True, status_code=200)
        users = User.objects.all()
        paginator = Paginator(users, limit)
        try:
            users_paginated = paginator.page(page)
        except PageNotAnInteger:
            users_paginated = paginator.page(1)
        except EmptyPage:
            users_paginated = []
        serializer = UserSerializerResponse(users_paginated, many=True)
        data_paginated = {
            'users': serializer.data,
            'paginations': {
                'document': len(serializer.data),
                'total_pages': paginator.num_pages,
                'current_page': users_paginated.number,
                'limit': limit
            }
        }
        set_cached_data(cache_key, data_paginated, settings.CACHE_TTL)
        return api_response(data=data_paginated, success=True, status_code=200)
    except User.DoesNotExist:
        return api_response(message="Users not found", success=False, status_code=404)

@extend_schema(
    responses={
        200: UserSerializerResponse,
        404: OpenApiResponse(description='User not found')
    },
    description="Endpoint to get the details of a specific user by their ID. Requires user validation.",
    summary="Get user details by ID",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idUser',
            required=True,
            type=int,
            location=OpenApiParameter.PATH
        )
    ]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
def get_user(request, idUser):
    try:
        cache_key = generate_cache_key('users-by-id', idUser=idUser)
        cached_data = get_cached_data(cache_key)
        if cached_data:
            return api_response(data=cached_data, success=True, status_code=200)
        user = User.objects.get(idUser=idUser)
        serializer = UserSerializerResponse(user)
        set_cached_data(cache_key, serializer.data, settings.CACHE_TTL)
        return api_response(data=serializer.data, success=True, status_code=200)
    except User.DoesNotExist:
        return api_response(message="User not found", success=False, status_code=404)

@extend_schema(
    responses={
        200: RoleSerializer,
        404: OpenApiResponse(description='Role not found')
    },
    description="Endpoint to retrieve a role by its ID. Requires authentication.",
    summary="Get role by ID",
    parameters=[
        OpenApiParameter(
            name='idRole',
            required=True,
            type=int,
            location=OpenApiParameter.PATH
        ),
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        )
    ]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
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

@extend_schema(
    responses={
        200: RoleSerializer(many=True),
        404: OpenApiResponse(description='Roles not found')
    },
    description="Endpoint to retrieve all roles. Requires authentication.",
    summary="Get all roles",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        )
    ]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
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

@extend_schema(
    responses={
        200: OpenApiResponse(description='Role updated'),
        404: OpenApiResponse(description='Role not found')
    },
    description="Endpoint to update a role by its ID. Requires authentication.",
    summary="Update role",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idRole',
            required=True,
            type=int,
            location=OpenApiParameter.PATH
        )
    ]
)
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
@checkAdmin
def update_role(request, idRole):
    try:
        role = Role.objects.get(idRole=idRole)
        data = request.data
        serializer = RoleSerializer(role, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return api_response(message="Role updated", success=True, status_code=200)
        return api_response(message=serializer.errors, success=False, status_code=400)
    except Role.DoesNotExist:
        return api_response(message="Role not found", success=False, status_code=404)
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        201: RoleSerializer,
        400: OpenApiResponse(description='Invalid input data'),
        404: OpenApiResponse(description='Role not found')
    },
    description="Endpoint to create a new role. Requires authentication.",
    summary="Create role",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        )
    ]
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
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