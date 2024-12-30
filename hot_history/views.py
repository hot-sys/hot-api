
from rest_framework.decorators import api_view, authentication_classes, parser_classes
from utils.token_required import token_required
from utils.api_response import api_response
from rest_framework.authentication import TokenAuthentication
from hot_users.decorators.checkUser import checkUser
from hot_users.decorators.checkAdmin import checkAdmin
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from .models import typeHistorique, Historique
from .serializers import typeHistoriqueSerializer, HistoriqueSerializer, CreateHistoriqueDTO
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta
from utils.cache_utils import generate_cache_key, get_cached_data, set_cached_data, delete_cache_by_prefix, list_cached_keys_by_prefix
from django.conf import settings

def create_history(idAdmin, idType, idCommande, description):
    try:
        typeStory = typeHistorique.objects.get(idType=idType)
        if typeStory.idType == 1:
            Historique.objects.create(
                idAdmin=idAdmin,
                idType=typeStory,
                idCommandeRoom=idCommande,
                description=description
            )
        elif typeStory.idType == 2:
            Historique.objects.create(
                idAdmin=idAdmin,
                idType=typeStory,
                idCommandeService=idCommande,
                description=description
            )
        return True
    except typeHistorique.DoesNotExist:
        return False

@extend_schema(
    responses={
        200: OpenApiResponse(description="History list"),
        500: OpenApiResponse(description="Internal server error"),
    },
    description="Get all history transaction",
    summary="Get all history transaction",
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
def get_all_history(request):
    try:
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        cache_key = generate_cache_key('history-getall', page, limit)
        cache_date = get_cached_data(cache_key)
        if cache_date:
            return api_response(data=cache_date, message="History list", success=True, status_code=200)

        history = Historique.objects.all()
        paginator = Paginator(history, limit)
        try:
            history_paginated = paginator.page(page)
        except PageNotAnInteger:
            history_paginated = paginator.page(1)
        except EmptyPage:
            history_paginated = []
        serializer = HistoriqueSerializer(history_paginated, many=True)
        data_paginated = {
            'history': serializer.data,
            'paginations': {
                'document': len(serializer.data),
                'total_pages': paginator.num_pages,
                'current_page': history_paginated.number,
                'limit': limit
            }
        }
        set_cached_data(cache_key, data_paginated, timeout=settings.CACHE_TTL)
        return api_response(data=data_paginated, message="History list", success=True, status_code=200)
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="History list user"),
        500: OpenApiResponse(description="Internal server error"),
    },
    description="Get all history transaction by user",
    summary="Get all history transaction by user",
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
def get_all_history_user(request):
    try:
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        idUser = request.idUser
        cache_key = generate_cache_key('history-user', idUser=idUser, page=page, limit=limit)
        cache_date = get_cached_data(cache_key)
        if cache_date:
            return api_response(data=cache_date, message="History list user", success=True, status_code=200)
        history = Historique.objects.filter(idAdmin=idUser)
        paginator = Paginator(history, limit)
        try:
            history_paginated = paginator.page(page)
        except PageNotAnInteger:
            history_paginated = paginator.page(1)
        except EmptyPage:
            history_paginated = []
        serializer = HistoriqueSerializer(history_paginated, many=True)
        data_paginated = {
            'history': serializer.data,
            'paginations': {
                'document': len(serializer.data),
                'total_pages': paginator.num_pages,
                'current_page': history_paginated.number,
                'limit': limit
            }
        }
        set_cached_data(cache_key, data_paginated, timeout=settings.CACHE_TTL)
        return api_response(data=data_paginated, message="History list user", success=True, status_code=200)
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)
@extend_schema(
    responses={
        200: OpenApiResponse(description="History list user"),
        500: OpenApiResponse(description="Internal server error"),
    },
    description="Get all history transaction by user",
    summary="Get all history transaction by user",
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
            location=OpenApiParameter.QUERY
        )
    ]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
@checkAdmin
def get_all_history_by_user(request, idUser):
    try:
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        cache_key = generate_cache_key('history-user', idUser=idUser, page=page, limit=limit)
        cache_date = get_cached_data(cache_key)
        if cache_date:
            return api_response(data=cache_date, message="History list user", success=True, status_code=200)
        history = Historique.objects.filter(idAdmin=idUser)
        paginator = Paginator(history, limit)
        try:
            history_paginated = paginator.page(page)
        except PageNotAnInteger:
            history_paginated = paginator.page(1)
        except EmptyPage:
            history_paginated = []
        serializer = HistoriqueSerializer(history_paginated, many=True)
        data_paginated = {
            'history': serializer.data,
            'paginations': {
                'document': len(serializer.data),
                'total_pages': paginator.num_pages,
                'current_page': history_paginated.number,
                'limit': limit
            }
        }
        set_cached_data(cache_key, data_paginated, timeout=settings.CACHE_TTL)
        return api_response(data=data_paginated, message="History list user", success=True, status_code=200)
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
        serializer = typeHistoriqueSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return api_response(message="Type created", success=True, status_code=201)
        return api_response(message=serializer.errors, success=False, status_code=400)
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Type updated"),
        404: OpenApiResponse(description="Type not found"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Update a type for admin",
    summary="Update type",
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
def update(request, idType):
    try:
        typeStory = typeHistorique.objects.get(idType=idType)
        data = request.data
        serializer = typeHistoriqueSerializer(typeStory, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return api_response(data= serializer.data,message="Type updated", success=True, status_code=200)
        return api_response(message=serializer.errors, success=False, status_code=400)
    except typeHistorique.DoesNotExist:
        return api_response(message="Type not found", success=False, status_code=404)
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)


@extend_schema(
    responses={
        200: OpenApiResponse(description="Type list"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get all type",
    summary="Get all type",
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
def get_all(request):
    try:
        status = typeHistorique.objects.all()
        serializer = typeHistoriqueSerializer(status, many=True)
        return api_response(data=serializer.data, message="Type list", success=True, status_code=200)
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Type list"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get type by Id",
    summary="Get type by Id",
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
def get_by_id(request, idType):
    try:
        status = typeHistorique.objects.get(idType=idType)
        serializer = typeHistoriqueSerializer(status)
        return api_response(data=serializer.data, message="Type found", success=True, status_code=200)
    except typeHistorique.DoesNotExist:
        return api_response(message="Type not found", success=False, status_code=404)