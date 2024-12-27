from rest_framework.decorators import api_view, authentication_classes, parser_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from utils.token_required import token_required
from utils.api_response import api_response
from rest_framework.authentication import TokenAuthentication
from hot_users.decorators.checkUser import checkUser
from hot_users.decorators.checkAdmin import checkAdmin
from hot_users.models import User
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from .models import Room, RoomImage, CommandeRoom
from .serializers import CommandeRoomSerializer, RoomSerializer, RoomImageSerializer, RoomResponseSerializer, CreateRoomDTO, UpdateRoomDTO, CreateCommandeDTO
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from datetime import datetime, timedelta
from utils.services.supabase_room_service import upload_images, remove_file
from django.db.models import Q
from hot_history.views import create_history


# COMMAND API
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
@extend_schema(
    request=CreateCommandeDTO,
    responses={
        200: OpenApiResponse(description="Commande created successfully"),
        400: OpenApiResponse(description="Invalid data")
    },
    description="Create a commande",
    summary="Create a commande",
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
def commande(request):
    data = request.data
    dto = CreateCommandeDTO(data=data)
    if dto.is_valid():
        validated_data = dto.validated_data
        idAdmin = request.idUser
        with transaction.atomic():
            price = Room.objects.get(idRoom=validated_data['idRoom']).price
            diffDays = int((validated_data['DateEnd'] - validated_data['DateStart']).days)
            if diffDays == 0:
                diffDays = 1
            total = price * diffDays
            commande = CommandeRoom.objects.create(
                idRoom_id=validated_data['idRoom'],
                idClient_id=validated_data['idClient'],
                idAdmin_id=idAdmin,
                idStatus_id=validated_data['idStatus'],
                DateStart=validated_data['DateStart'],
                DateEnd=validated_data['DateEnd'],
                price=price,
                total=total
            )
            if validated_data['idStatus'] == 3:
                room = Room.objects.get(idRoom=validated_data['idRoom'])
                room.available = False
                room.dateAvailable = validated_data['DateEnd'] + timedelta(hours=5)
                room.save()
            try:
                admin = User.objects.get(idUser=idAdmin)
                create_history(admin, 1, commande, "Commande created")
            except User.DoesNotExist:
                return api_response(data=None, message="Admin not found", success=False, status_code=404)
            serializer = CommandeRoomSerializer(commande)
        return api_response(data=serializer.data, message="Commande created successfully", success=True, status_code=200)
    else:
        return api_response(data=None, message=dto.errors, success=False, status_code=400)

@extend_schema(
    request=CreateCommandeDTO,
    responses={
        200: OpenApiResponse(description="Commande reserved successfully"),
        400: OpenApiResponse(description="Invalid data")
    },
    description="Create a commande with status reserved",
    summary="Create a commande with status reserved",
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
def reserved(request):
    try:
        data = request.data
        dto = CreateCommandeDTO(data=data)
        idUser = request.idUser
        if dto.is_valid():
            validated_data = dto.validated_data
            with transaction.atomic():
                price = Room.objects.get(idRoom=validated_data['idRoom']).price
                total = price * (validated_data['DateEnd'] - validated_data['DateStart']).days
                commande = CommandeRoom.objects.create(
                    idRoom_id=validated_data['idRoom'],
                    idClient_id=idUser,
                    idStatus_id=1,
                    DateStart=validated_data['DateStart'],
                    DateEnd=validated_data['DateEnd'],
                    price=price,
                    total=total
                )
                serializer = CommandeRoomSerializer(commande)
            return api_response(data=serializer.data, message="Commande reserved successfully", success=True, status_code=200)
        else:
            return api_response(data=None, message=dto.errors, success=False, status_code=400)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

@extend_schema(
    request=CreateCommandeDTO,
    responses={
        200: OpenApiResponse(description="Commande before create"),
        400: OpenApiResponse(description="Invalid data")
    },
    description="Simulate a commande",
    summary="Simulate a commande",
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
def simulate_commande(request):
    data = request.data
    dto = CreateCommandeDTO(data=data)
    if dto.is_valid():
        validated_data = dto.validated_data
        idAdmin = request.idUser
        with transaction.atomic():
            price = Room.objects.get(idRoom=validated_data['idRoom']).price
            total = price * (validated_data['DateEnd'] - validated_data['DateStart']).days
            commande = {
                "idRoom_id" : validated_data['idRoom'],
                "idClient_id" : validated_data['idClient'],
                "idAdmin_id" : idAdmin,
                "idStatus_id" : validated_data['idStatus'],
                "DateStart" : validated_data['DateStart'],
                "DateEnd" : validated_data['DateEnd'],
                "price" : price,
                "total" : total
            }
        return api_response(data=commande, message="Commande before create", success=True, status_code=200)
    else:
        return api_response(data=None, message=dto.errors, success=False, status_code=400)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Commande confirmed successfully"),
        404: OpenApiResponse(description="Commande not found"),
    },
    description="Confirm a commande by ID",
    summary="Confirm commande",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idCommande',
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
def confirmeCommande(request, idCommande):
    try:
        commande = CommandeRoom.objects.get(idCommande=idCommande)
        if commande.idStatus_id == 3:
            return api_response(data=None, message="Commande already confirmed", success=False, status_code=400)
        commande.idStatus_id = 3
        commande.save()
        room = Room.objects.get(idRoom=commande.idRoom_id)
        room.available = False
        room.dateAvailable = commande.DateEnd + timedelta(hours=5)
        room.save()
        serializer = CommandeRoomSerializer(commande)
        try:
            idAdmin = request.idUser
            admin = User.objects.get(idUser=idAdmin)
            create_history(admin, 1, commande, "Commande confirmed")
        except User.DoesNotExist:
            return api_response(data=None, message="Admin not found", success=False, status_code=404)
        return api_response(data=serializer.data, message="Commande confirmed successfully", success=True, status_code=200)
    except CommandeRoom.DoesNotExist:
        return api_response(data=None, message="Commande not found", success=False, status_code=404)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="All commandes"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get all commandes with paginate data",
    summary="Get all commandes",
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
def get_commande(request):
    try:
        commande = CommandeRoom.objects.all()

        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        paginator = Paginator(commande, limit)
        try:
            commande_paginated = paginator.page(page)
        except PageNotAnInteger:
            commande_paginated = paginator.page(1)
        except EmptyPage:
            commande_paginated = []

        serializer = CommandeRoomSerializer(commande_paginated, many=True)
        data_paginated = {
            'commande': serializer.data,
            'paginations': {
                'document': len(serializer.data),
                'total_pages': paginator.num_pages,
                'current_page': commande_paginated.number,
                'limit': limit
            }
        }
        return api_response(data=data_paginated, message="All commande room", success=True, status_code=200)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="All commandes without paginate"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get all commandes without paginate data",
    summary="Get all commandes",
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
def get_all_commande(request):
    try:
        commande = CommandeRoom.objects.all()

        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        paginator = Paginator(commande, limit)
        try:
            commande_paginated = paginator.page(page)
        except PageNotAnInteger:
            commande_paginated = paginator.page(1)
        except EmptyPage:
            commande_paginated = []

        serializer = CommandeRoomSerializer(commande, many=True)
        data_paginated = {
            'commande': serializer.data,
            'paginations': {
                'document': len(serializer.data),
                'total_pages': paginator.num_pages,
                'current_page': commande_paginated.number,
                'limit': limit
            }
        }
        return api_response(data=data_paginated, message="All commande room", success=True, status_code=200)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Commande retrieved successfully"),
        404: OpenApiResponse(description="Commande not found"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get a commande by ID",
    summary="Get commande",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idCommande',
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
def get_commande_by_id(request, idCommande):
    try:
        commande = CommandeRoom.objects.get(idCommande=idCommande)
        serializer = CommandeRoomSerializer(commande)
        return api_response(data=serializer.data, message="Commande retrieved successfully", success=True, status_code=200)
    except CommandeRoom.DoesNotExist:
        return api_response(data=None, message="Commande not found", success=False, status_code=404)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)


@extend_schema(
    request="query",
    responses={
        200: OpenApiResponse(description="Commande filtered successfully"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Filter commandes by parameters",
    summary="Filter commandes",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
    ]
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
@checkAdmin
def filter_commande(request):
    try:
        filter_params = request.data.get('filters', {})
        commande_queryset = CommandeRoom.objects.filter(**filter_params)

        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        paginator = Paginator(commande_queryset, limit)
        try:
            commande_paginated = paginator.page(page)
        except PageNotAnInteger:
            commande_paginated = paginator.page(1)
        except EmptyPage:
            commande_paginated = []

        serializer = CommandeRoomSerializer(commande_paginated, many=True)
        data_paginated = {
            'commande filter': serializer.data,
            'paginations': {
                'document': len(serializer.data),
                'total_pages': paginator.num_pages,
                'current_page': commande_paginated.number,
                'limit': limit
            }
        }

        return api_response(data=data_paginated, message="Commande retrieved successfully", success=True, status_code=200)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

# ROOM API
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
@extend_schema(
    request=CreateRoomDTO,
    responses={
        200: OpenApiResponse(description="Room created"),
        500: OpenApiResponse(description="Internal server error")
    },
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
        ),
        OpenApiParameter(
            name='idRoom',
            required=True,
            type=int,
            location=OpenApiParameter.PATH
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
        ),
        OpenApiParameter(
            name='idImage',
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

        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
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
                'document': len(serializer.data),
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
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
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
        200: OpenApiResponse(description="All images for an room"),
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
        ),
        OpenApiParameter(
            name='idRoom',
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
def image_room(request, idRoom):
    try:
        try:
            room = Room.objects.get(idRoom=idRoom)
        except Room.DoesNotExist:
            return api_response(data=None, message="Room not found", success=False, status_code=404)
        imageRoom = RoomImage.objects.filter(idRoom=idRoom)
        serializer = RoomImageSerializer(imageRoom, many=True)
        return api_response(data=serializer.data, message="All images for an room", success=True, status_code=200)
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
        ),
        OpenApiParameter(
            name='idRoom',
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
def get_room(request, idRoom):
    try:
        room = Room.objects.get(idRoom=idRoom)
        serializer = RoomResponseSerializer(room)
        imageRome = RoomImage.objects.filter(idRoom=idRoom)
        serializerRoom = RoomImageSerializer(imageRome, many=True)
        data = {
            'Room': serializer.data,
            'images': serializerRoom.data
        }
        return api_response(data=data, message="Room retrieved successfully", success=True, status_code=200)
    except Room.DoesNotExist:
        return api_response(data=None, message="Room not found", success=False, status_code=404)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Room unavailable retrieved successfully"),
        404: OpenApiResponse(description="Room not found")
    },
    description="Get room with unavailable true",
    summary="Get room unavailable",
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
def room_unavailable(request):
    try:
        rooms = Room.objects.filter(available=False)

        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
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
                'document': len(serializer.data),
                'total_pages': paginator.num_pages,
                'current_page': rooms_paginated.number,
                'limit': limit
            }
        }
        return api_response(data=data_paginated, message="Rooms unavailable retrieved successfully", success=True, status_code=200)
    except Room.DoesNotExist:
        return api_response(data=None, message="Room not found", success=False, status_code=404)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Room available retrieved successfully"),
        404: OpenApiResponse(description="Room not found")
    },
    description="Get room with available true",
    summary="Get room available",
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
def room_available(request):
    try:
        rooms = Room.objects.filter(available=True)

        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
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
                'document': len(serializer.data),
                'total_pages': paginator.num_pages,
                'current_page': rooms_paginated.number,
                'limit': limit
            }
        }
        return api_response(data=data_paginated, message="Rooms available retrieved successfully", success=True, status_code=200)
    except Room.DoesNotExist:
        return api_response(data=None, message="Room not found", success=False, status_code=404)

@extend_schema(
    request="query",
    responses={
        200: OpenApiResponse(description="Rooms retrieved successfully"),
        400: OpenApiResponse(description="Query is required")
    },
    description="Search rooms by query",
    summary="Search rooms",
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
def search_room(request):
    data = request.data
    if 'query' in data:
        query = data['query']

        rooms = Room.objects.filter(
            Q(title__icontains=query) |
            Q(subTitle__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query)
        )

        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
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
                'document': len(serializer.data),
                'total_pages': paginator.num_pages,
                'current_page': rooms_paginated.number,
                'limit': limit
            }
        }
        return api_response(data=data_paginated, message="Rooms search retrieved successfully", success=True, status_code=200)
    else:
        return api_response(data=None, message="Query is required", success=False, status_code=400)

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
        ),
        OpenApiParameter(
            name='idRoom',
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
        200: OpenApiResponse(description="Room freed successfully"),
        404: OpenApiResponse(description="Room not found")
    },
    description="Free a room by ID",
    summary="Free room",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        ),
        OpenApiParameter(
            name='idRoom',
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
def free_room(request, idRoom):
    try:
        room = Room.objects.get(idRoom=idRoom)
        room.available = True
        room.dateAvailable = None
        room.save()
        return api_response(data=None, message="Room freed successfully", success=True, status_code=200)
    except Room.DoesNotExist:
        return api_response(data=None, message="Room not found", success=False, status_code=404)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

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
        ),
        OpenApiParameter(
            name='idRoom',
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
        ),
        OpenApiParameter(
            name='idRoom',
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