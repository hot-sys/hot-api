from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from hot_users.models import Role
from hot_services.serializers import StatusSerializer
from hot_users.models import User, Role
from hot_users.serializers import CreateUserSerializer, UserSerializerResponse, RoleSerializer, RegisterDTO, UpdateUserDto, RoleDTO, UpdatePosteDTO
from hot_history.serializers import typeHistoriqueSerializer
from hot_history.models import typeHistorique
from hot_services.models import Status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils.api_response import api_response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

@extend_schema(
    responses={
        200: UserSerializerResponse(many=True),
        404: OpenApiResponse(description='Users not found')
    },
    description="Endpoint to get all registered users. Requires admin privileges.",
    summary="Get all users",
)
@api_view(['GET'])
def get_all_users(request):
    try:
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
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
        return api_response(data=data_paginated, success=True, status_code=200)
    except User.DoesNotExist:
        return api_response(message="Users not found", success=False, status_code=404)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Type list"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get all type",
    summary="Get all type",
)
@api_view(['GET'])
def get_all_typeHistorique(request):
    try:
        status = typeHistorique.objects.all()
        serializer = typeHistoriqueSerializer(status, many=True)
        return api_response(data=serializer.data, message="Type list", success=True, status_code=200)
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Status list"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get all status",
    summary="Get all status",
)
@api_view(['GET'])
def get_all_status(request):
    try:
        status = Status.objects.all()
        serializer = StatusSerializer(status, many=True)
        return api_response(data=serializer.data, message="Status list", success=True, status_code=200)
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: RoleSerializer(many=True),
        404: OpenApiResponse(description='Roles not found')
    },
    description="Endpoint to retrieve all roles. Requires authentication.",
    summary="Get all roles",
)
@api_view(['GET'])
def get_all_roles(request):
    try:
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return api_response(data=serializer.data)
    except Role.DoesNotExist:
        return api_response(message="Roles not found", success=False, status_code=404)

@extend_schema(
    request=RegisterDTO,
    responses={
        201: CreateUserSerializer,
        400: OpenApiResponse(description='Invalid input data or user data')
    },
    description="Endpoint to Init a new user. The user must provide the necessary registration data.",
    summary="Init new user",
)
@api_view(['POST'])
def createUser(request):
    data = request.data
    dto = RegisterDTO(data=data)
    if dto.is_valid():
        validated_data = dto.validated_data
        validated_data['password'] = make_password(validated_data['password'])
        serializer = CreateUserSerializer(data=validated_data)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, message="User registered successfully", success=True, status_code=201)
        return api_response(data=serializer.errors, message="Invalid user data", success=False, status_code=400)
    return api_response(data=dto.errors, message="Invalid input data", success=False, status_code=400)

@extend_schema(
    responses={
        201: RoleSerializer,
        400: OpenApiResponse(description='Invalid input data'),
        404: OpenApiResponse(description='Role not found')
    },
    description="Endpoint to Init a new role. Requires authentication.",
    summary="Init role",
)
@api_view(['POST'])
def createRole(request):
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

@extend_schema(
    request=StatusSerializer,
    responses={
        200: OpenApiResponse(description="Status created"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Init a status for admin",
    summary="Init status",
)
@api_view(['POST'])
def createStatus(request):
    try:
        data = request.data
        serializer = StatusSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return api_response(message="Status created", success=True, status_code=201)
        return api_response(message=serializer.errors, success=False, status_code=400)
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)

@extend_schema(
    request=typeHistoriqueSerializer,
    responses={
        200: OpenApiResponse(description="Type created"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Create a type for history transaction",
    summary="Create type",
)
@api_view(['POST'])
def createTypeHistory(request):
    try:
        data = request.data
        serializer = typeHistoriqueSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return api_response(message="Type created", success=True, status_code=201)
        return api_response(message=serializer.errors, success=False, status_code=400)
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)