from rest_framework.decorators import api_view, authentication_classes
from utils.token_required import token_required
from utils.api_response import api_response
from rest_framework.authentication import TokenAuthentication
from hot_users.decorators.checkUser import checkUser
from hot_users.decorators.checkAdmin import checkAdmin
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from .models import Room
from .serializers import RoomSerializer, CreateRoomDTO
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction

@extend_schema(
    request=CreateRoomDTO,
    responses={200: OpenApiResponse(description="Room created")},
    description="Create a room with the given data",
    summary="Create room",
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
        dto = CreateRoomDTO(data=data)
        if dto.is_valid():
            with transaction.atomic():
                room = Room.objects.create(
                    idAdmin_id=request.userInstance.idUser,
                    title=dto.validated_data['title'],
                    subTitle=dto.validated_data.get('subTitle'),
                    description=dto.validated_data['description'],
                    price=dto.validated_data['price'],
                    available=dto.validated_data['available'],
                    dateAvailable=dto.validated_data.get('dateAvailable'),
                    info=dto.validated_data.get('info')
                )
                serializer = RoomSerializer(room)
            return api_response(message="Create room successfully" ,data=serializer.data, success=True, status_code=200)
        else:
            return api_response(message=dto.errors, success=False, status_code=400)
    except Exception as e:
        return api_response(message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="All rooms")
    },
    description="Get all rooms with paginate data",
    summary="Get all rooms",
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
def all(request):
    try:
        rooms = Room.objects.all().select_related('idAdmin')
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        paginator = Paginator(rooms, limit)
        try:
            rooms_paginated = paginator.page(page)
        except PageNotAnInteger:
            rooms_paginated = paginator.page(1)
        except EmptyPage:
            rooms_paginated = []

        serializer = RoomSerializer(rooms_paginated, many=True)
        data_paginated = {
            'rooms': serializer.data,
            'paginations': {
                'total_pages': paginator.num_pages,
                'current_page': rooms_paginated.number,
                'limit': limit
            }
        }
        return api_response(data=data_paginated, message="All rooms", success=True, status_code=200)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Room retrieved successfully"),
        404: OpenApiResponse(description="Room not found")
    },
    description="Get a single room by ID",
    summary="Get room",
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
def getRoom(request, idRoom):
    try:
        room = Room.objects.get(idRoom=idRoom)
        serializer = RoomSerializer(room)
        return api_response(data=serializer.data, message="Room retrieved successfully", success=True, status_code=200)
    except Room.DoesNotExist:
        return api_response(data=None, message="Room not found", success=False, status_code=404)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)