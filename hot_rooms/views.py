from rest_framework.decorators import api_view, authentication_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from utils.token_required import token_required
from utils.api_response import api_response
from rest_framework.authentication import TokenAuthentication
from hot_users.decorators.checkUser import checkUser
from hot_users.decorators.checkAdmin import checkAdmin
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from .models import Room, RoomImage
from .serializers import RoomSerializer, RoomImageSerializer, RoomResponseSerializer, CreateRoomDTO, UpdateRoomDTO
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from datetime import datetime, timedelta
from utils.services.supabase_room_service import upload_images, remove_file

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
    request=MultiPartParser,
    responses={
        200: OpenApiResponse(description="Images uploaded successfully"),
        404: OpenApiResponse(description="Room not found"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Upload images for a room",
    summary="Upload images",
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
@parser_classes([MultiPartParser, FormParser])
def createimage(request, idRoom):
    try:
        room = Room.objects.get(idRoom=idRoom)
        files = request.FILES.getlist('images')
        if not files:
            return api_response(data=None, message="No images uploaded", success=False, status_code=400)
        urls = upload_images(files)
        for url in urls:
            RoomImage.objects.create(idRoom=room, image=url)
        return api_response(data=urls, message="Images uploaded successfully", success=True, status_code=200)
    except Room.DoesNotExist:
        return api_response(data=None, message="Room not found", success=False, status_code=404)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Image deleted successfully"),
        404: OpenApiResponse(description="Image not found"),
        500: OpenApiResponse(description="Internal server error"),
    },
    description="Delete an image by ID",
    summary="Delete image",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        )
    ]
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
@checkAdmin
def delete_image(request, idImage):
    try:
        image = RoomImage.objects.get(idImage=idImage)
        result = remove_file(image.image)
        image.delete()
        return api_response(data=result, message="Image deleted successfully", success=True, status_code=200)
    except RoomImage.DoesNotExist:
        return api_response(data=None, message="Image not found", success=False, status_code=404)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)


@extend_schema(
    request=MultiPartParser,
    responses={200: OpenApiResponse(description="Images uploaded successfully")},
    description="Upload images for a room",
    summary="Upload images",
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
@parser_classes([MultiPartParser, FormParser])
def upload(request):
    try:
        files = request.FILES.getlist('images')
        if not files:
            return api_response(data=None, message="No images uploaded", success=False, status_code=400)
        urls = upload_images(files)
        return api_response(data=urls, message="Images uploaded successfully", success=True, status_code=200)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

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

        serializer = RoomResponseSerializer(rooms_paginated, many=True)
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
        200: OpenApiResponse(description="All images"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get all images",
    summary="Get images",
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
def imageall(request):
    try:
        imageRoom = RoomImage.objects.all()
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        paginator = Paginator(imageRoom, limit)

        try:
            imageRoom_paginated = paginator.page(page)
        except PageNotAnInteger:
            imageRoom_paginated = paginator.page(1)
        except EmptyPage:
            imageRoom_paginated = []

        serializer = RoomImageSerializer(imageRoom, many=True)
        data_paginated = {
            'images': serializer.data,
            'paginations': {
                'document': len(serializer.data),
                'total_pages': paginator.num_pages,
                'current_page': imageRoom_paginated.number,
                'limit': limit
            }
        }
        return api_response(data=serializer.data, message="All images", success=True, status_code=200)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)


@extend_schema(
    responses={
        200: OpenApiResponse(description="All images for an image"),
        404: OpenApiResponse(description="Room not found"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get all images for a room",
    summary="Get images for a room",
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
def image_room(request, idRoom):
    try:
        try:
            room = Room.objects.get(idRoom=idRoom)
        except Room.DoesNotExist:
            return api_response(data=None, message="Room not found", success=False, status_code=404)
        imageRoom = RoomImage.objects.filter(idRoom=idRoom)
        serializer = RoomImageSerializer(imageRoom, many=True)
        return api_response(data=serializer.data, message="All images for an image", success=True, status_code=200)
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
def get_room(request, idRoom):
    try:
        room = Room.objects.get(idRoom=idRoom)
        serializer = RoomResponseSerializer(room)
        return api_response(data=serializer.data, message="Room retrieved successfully", success=True, status_code=200)
    except Room.DoesNotExist:
        return api_response(data=None, message="Room not found", success=False, status_code=404)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

@extend_schema(
    request=UpdateRoomDTO,
    responses={
        200: OpenApiResponse(description="Room updated successfully"),
        404: OpenApiResponse(description="Room not found")
    },
    description="Update a room by ID",
    summary="Update room",
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
def update_by_admin(request, idRoom):
    data = request.data
    if 'idAdmin' in data:
        return api_response(data=None, message="You can't update room admin", success=False, status_code=403)

    dto = UpdateRoomDTO(data=data)
    if dto.is_valid():
        validated_data = dto.validated_data
        try:
            room = Room.objects.get(idRoom=idRoom)
            currentUser = request.idUser
            if room.idAdmin_id != currentUser:
                return api_response(data=None, message="You can't update this room", success=False, status_code=403)
            for key, value in validated_data.items():
                setattr(room, key, value)
            room.save()
            serializer = RoomResponseSerializer(room)
            return api_response(data=serializer.data, message="Room updated successfully", success=True, status_code=200)
        except Room.DoesNotExist:
            return api_response(data=None, message="Room not found", success=False, status_code=404)
    else:
        return api_response(data=None, message=dto.errors, success=False, status_code=400)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Room deleted successfully"),
        404: OpenApiResponse(description="Room not found")
    },
    description="Delete a room by ID",
    summary="Delete room",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        )
    ]
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
@checkAdmin
def delete_by_admin(request, idRoom):
    try:
        currentUser = request.idUser
        room = Room.objects.get(idRoom=idRoom)
        if room.idAdmin_id!= currentUser:
            return api_response(data=None, message="You can't delete this room", success=False, status_code=403)
        room.deletedAt = datetime.now()
        room.save()
        return api_response(data=None, message="Room deleted successfully", success=True, status_code=200)
    except Room.DoesNotExist:
        return api_response(data=None, message="Room not found", success=False, status_code=404)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Room recovered successfully"),
        404: OpenApiResponse(description="Room not found")
    },
    description="Recover a deleted room by ID",
    summary="Recover room",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        )
    ]
)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
@checkAdmin
def recover_by_admin(request, idRoom):
    try:
        currentUser = request.idUser
        room = Room.all_objects.get(idRoom=idRoom)
        if room.idAdmin_id != currentUser:
            return api_response(data=None, message="You can't recover this room", success=False, status_code=403)
        room.deletedAt = None
        room.save()
        return api_response(data=None, message="Room recovered successfully", success=True, status_code=200)
    except Room.DoesNotExist:
        return api_response(data=None, message="Room not found", success=False, status_code=404)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)