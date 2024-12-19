from utils.api_response import api_response
from rest_framework.decorators import api_view, authentication_classes, parser_classes
from utils.token_required import token_required
from hot_users.decorators.checkUser import checkUser
from hot_users.decorators.checkAdmin import checkAdmin
from rest_framework.authentication import TokenAuthentication
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Client
from .serializers import ClientSerializer, CreateClientDTO, UpdateClientDTO
from django.db import transaction
from django.db.models import Q
from datetime import datetime, timedelta

@extend_schema(
    responses={
        200: OpenApiResponse(description="Clients retrieved successfully"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get all clients in the system",
    summary="Get all clients",
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
def all(request):
    try:
        clients = Client.objects.all()

        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        paginator = Paginator(clients, limit)

        try:
            clients_paginated = paginator.page(page)
        except PageNotAnInteger:
            clients_paginated = paginator.page(1)
        except EmptyPage:
            clients_paginated = []

        serializer = ClientSerializer(clients, many=True)
        data_paginated = {
            'clients': serializer.data,
            'paginations': {
                'document': len(serializer.data),
                'total_pages': paginator.num_pages,
                'current_page': clients_paginated.number,
                'limit': limit
            }
        }
        return api_response(data=data_paginated, message="Clients retrieved successfully")
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Client retrieved successfully"),
        404: OpenApiResponse(description="Client not found")
    },
    description="Get a client by id",
    summary="Get a client by id",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idClient',
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
def get_by_id(request, idClient):
    try:
        client = Client.objects.get(idClient=idClient)
        serializer = ClientSerializer(client)
        return api_response(data=serializer.data, message="Client retrieved successfully")
    except Client.DoesNotExist:
        return api_response(message="Client not found", success=False, status_code=404)

@extend_schema(
    request=UpdateClientDTO,
    responses={
        200: OpenApiResponse(description="Client updated successfully"),
        400: OpenApiResponse(description="Bad request"),
        404: OpenApiResponse(description="Client not found")
    },
    description="Update a client by id",
    summary="Update a client by id",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idClient',
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
def update(request, idClient):
    data = request.data
    dto = UpdateClientDTO(data=data)
    if dto.is_valid():
        validated_data = dto.validated_data
        try:
            client = Client.objects.get(idClient=idClient)
            for key, value in validated_data.items():
                setattr(client, key, value)
            client.save()
            serializer = ClientSerializer(client)
            return api_response(data=serializer.data, message="Client updated successfully")
        except Client.DoesNotExist:
            return api_response(message="Client not found", success=False, status_code=404)
    else:
        return api_response(message=dto.errors, success=False, status_code=400)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Client deleted successfully"),
        404: OpenApiResponse(description="Client not found")
    },
    description="Delete a client by id",
    summary="Delete a client by id",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idClient',
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
def delete(request, idClient):
    try:
        client = Client.objects.get(idClient=idClient)
        client.deletedAt = datetime.now()
        client.save()
        return api_response(message="Client deleted successfully")
    except Client.DoesNotExist:
        return api_response(message="Client not found", success=False, status_code=404)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Client recovered successfully"),
        404: OpenApiResponse(description="Client not found")
    },
    description="Recover a client by id",
    summary="Recover a client by id",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idClient',
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
def recover(request, idClient):
    try:
        client = Client.all_objects.get(idClient=idClient)
        client.deletedAt = None
        client.save()
        return api_response(message="Client recovered successfully")
    except Client.DoesNotExist:
        return api_response(message="Client not found", success=False, status_code=404)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Client search retrieved successfully"),
        400: OpenApiResponse(description="Query is required")
    },
    description="Search clients by any field",
    summary="Search clients by any field",
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
def search(request):
    data = request.data
    if 'query' in data:
        query = data['query']
        clients = Client.objects.filter(
            Q(name__icontains=query) |
            Q(firstName__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query) |
            Q(adress__icontains=query)
        )

        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        paginator = Paginator(clients, limit)

        try:
            clients_paginated = paginator.page(page)
        except PageNotAnInteger:
            clients_paginated = paginator.page(1)
        except EmptyPage:
            clients_paginated = []

        serializer = ClientSerializer(clients_paginated, many=True)
        data_paginated = {
            'rooms': serializer.data,
            'paginations': {
                'document': len(serializer.data),
                'total_pages': paginator.num_pages,
                'current_page': clients_paginated.number,
                'limit': limit
            }
        }
        return api_response(data=data_paginated, message="Client search retrieved successfully", success=True, status_code=200)

    else:
        return api_response(data=None, message="Query is required", success=False, status_code=400)

@extend_schema(
    request=CreateClientDTO,
    responses={
        200: OpenApiResponse(description="Client created successfully"),
        400: OpenApiResponse(description="Bad request"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Create a new client in the system",
    summary="Create a new client",
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
    try:
        data = request.data
        dto = CreateClientDTO(data=data)
        if not dto.is_valid():
            return api_response(message=dto.errors, success=False, status_code=400)
        with transaction.atomic():
            client = Client.objects.create(
                name=dto.validated_data['name'],
                firstName=dto.validated_data['firstName'],
                phone=dto.validated_data['phone'],
                email=dto.validated_data['email'],
                genre=dto.validated_data['genre'],
                adress=dto.validated_data['adress'],
                cin=dto.validated_data['cin']
            )
            serializer = ClientSerializer(client)
        return api_response(data=serializer.data, message="Client created successfully")
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)