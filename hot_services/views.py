
from rest_framework.decorators import api_view, authentication_classes, parser_classes
from utils.token_required import token_required
from utils.api_response import api_response
from rest_framework.authentication import TokenAuthentication
from hot_users.decorators.checkUser import checkUser
from hot_users.decorators.checkAdmin import checkAdmin
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Status, Service
from .serializers import StatusSerializer, ServiceSerializer, CreateServiceDTO
from django.db import transaction
from datetime import datetime, timedelta

# SERVICES API
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
@extend_schema(
    request=CreateServiceDTO,
    responses={
        201: OpenApiResponse(description="Service created"),
        400: OpenApiResponse(description="Bad request")
    },
    description="Create a service for admin",
    summary="Create service",
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
def create_service(request):
    data = request.data
    dto = CreateServiceDTO(data=data)
    if dto.is_valid():
        idUser = request.idUser
        with transaction.atomic():
            service = Service.objects.create(
                idUser_id=idUser,
                name=dto.validated_data['name'],
                description=dto.validated_data['description']
            )
            serializer = ServiceSerializer(service)
            return api_response(data=serializer.data, message="Service created", success=True, status_code=201)
    else:
        return api_response(message=dto.errors, success=False, status_code=400)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Service updated"),
        404: OpenApiResponse(description="Service not found"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Update a service for admin",
    summary="Update service",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idService',
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
def update_service(request, idService):
    try:
        service = Service.objects.get(idService=idService)
        data = request.data
        serializer = ServiceSerializer(service, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data, message="Service updated", success=True, status_code=200)
        return api_response(message=serializer.errors, success=False, status_code=400)
    except Service.DoesNotExist:
        return api_response(message="Service not found", success=False, status_code=404)
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)


@extend_schema(
    responses={
        200: OpenApiResponse(description="Service deleted"),
        404: OpenApiResponse(description="Service not found"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Recover a service for admin",
    summary="Recover service",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idService',
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
def delete_service(request, idService):
    try:
        service = Service.objects.get(idService=idService)
        service.deletedAt = datetime.now()
        service.save()
        return api_response(message="Service deleted", success=True, status_code=200)
    except Service.DoesNotExist:
        return api_response(message="Service not found", success=False, status_code=404)
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Service recovered"),
        404: OpenApiResponse(description="Service not found"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Recover a service for admin",
    summary="Recover service",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idService',
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
def recover_service(request, idService):
    try:
        service = Service.all_objects.get(idService=idService)
        service.deletedAt = None
        service.save()
        return api_response(message="Service recovered", success=True, status_code=200)
    except Service.DoesNotExist:
        return api_response(message="Service not found", success=False, status_code=404)
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Service list"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get all services",
    summary="Get all services",
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
def get_all_service(request):
    try:
        services = Service.objects.all()

        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        paginator = Paginator(services, limit)
        try:
            service_paginated = paginator.page(page)
        except PageNotAnInteger:
            service_paginated = paginator.page(1)
        except EmptyPage:
            service_paginated = []

        serializer = ServiceSerializer(service_paginated, many=True)
        data_paginated = {
            'services': serializer.data,
            'paginations': {
                'document': len(serializer.data),
                'total_pages': paginator.num_pages,
                'current_page': service_paginated.number,
                'limit': limit
            }
        }
        return api_response(data=data_paginated, message="Service list", success=True, status_code=200)
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Service found"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get service by id",
    summary="Get service by id",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idService',
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
@checkAdmin
def get_by_id_service(request, idService):
    try:
        service = Service.objects.get(idService=idService)
        serializer = ServiceSerializer(service)
        return api_response(data=serializer.data, message="Service found", success=True, status_code=200)
    except Service.DoesNotExist:
        return api_response(message="Service not found", success=False, status_code=404)


# STATUS API
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
@extend_schema(
    request=StatusSerializer,
    responses={
        200: OpenApiResponse(description="Status created"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Create a status for admin",
    summary="Create status",
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
def create_status(request):
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
    responses={
        200: OpenApiResponse(description="Status updated"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Update a status for admin",
    summary="Update status",
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
@checkAdmin
def update_status(request, idStatus):
    try:
        status = Status.objects.get(idStatus=idStatus)
        data = request.data
        serializer = StatusSerializer(status, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return api_response(data= serializer.data, message="Status updated", success=True, status_code=200)
        return api_response(message=serializer.errors, success=False, status_code=400)
    except Status.DoesNotExist:
        return api_response(message="Status not found", success=False, status_code=404)
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Status list"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get all status",
    summary="Get all status",
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
def get_all_status(request):
    try:
        status = Status.objects.all()
        serializer = StatusSerializer(status, many=True)
        return api_response(data=serializer.data, message="Status list", success=True, status_code=200)
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Status list"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get status by Id",
    summary="Get status by Id",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idStatus',
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
@checkAdmin
def get_by_id_status(request, idStatus):
    try:
        status = Status.objects.get(idStatus=idStatus)
        serializer = StatusSerializer(status)
        return api_response(data=serializer.data, message="Status found", success=True, status_code=200)
    except Status.DoesNotExist:
        return api_response(message="Status not found", success=False, status_code=404)