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
from django.utils.timezone import now
from utils.services.supabase_room_service import upload_images, remove_file
from django.db.models import Q
from hot_history.views import create_history, create_history_room
from utils.cache_utils import generate_cache_key, get_cached_data, set_cached_data, delete_cache_by_prefix, list_cached_keys_by_prefix
from django.conf import settings
from hot_clients.serializers import ClientSerializer
from hot_clients.models import Client

# STAT API
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
@extend_schema(
    responses={
        200: OpenApiResponse(description="Stat retrieved successfully"),
        400: OpenApiResponse(description="Bad Request"),
        401: OpenApiResponse(description="Unauthorized"),
        500: OpenApiResponse(description="Internal Server Error")
    },
    description="Get all stats",
    summary="Get stats",
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
def stat(request):
    try:
        cache_key = generate_cache_key('room-stat')
        data = get_cached_data(cache_key)
        if data is not None:
            return api_response(data=data, message="Stat retrieved from cache successfully", success=True, status_code=200)

        rooms = Room.objects.all()
        totalRoom = rooms.count()
        totalRoomAvailable = rooms.filter(available=True).count()
        totalRoomUnavailable = rooms.filter(available=False).count()
        totalCommande = CommandeRoom.objects.all().count()
        totalCommandeReserved = CommandeRoom.objects.filter(idStatus=1).count()
        totalCommandeCanceled = CommandeRoom.objects.filter(idStatus=2).count()
        totalCommandeConfirmed = CommandeRoom.objects.filter(idStatus=3).count()
        totalCommandePending = CommandeRoom.objects.filter(idStatus=4).count()

        data = {
            'totalRoom': totalRoom,
            'totalRoomAvailable': totalRoomAvailable,
            'totalRoomUnavailable': totalRoomUnavailable,
            'totalCommande': totalCommande,
            'totalCommandeConfirmed': totalCommandeConfirmed,
            'totalCommandeReserved': totalCommandeReserved,
            'totalCommandeCanceled': totalCommandeCanceled,
            'totalCommandePending': totalCommandePending
        }

        set_cached_data(cache_key, data, settings.CACHE_TTL)
        return api_response(data=data, message="Stat retrieved successfully", success=True, status_code=200)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

# COMMAND API
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

@extend_schema(
    responses={
        200: OpenApiResponse(description="Commande payed"),
        400: OpenApiResponse(description="Bad Request"),
        401: OpenApiResponse(description="Unauthorized"),
        404: OpenApiResponse(description="Commande not found"),
        500: OpenApiResponse(description="Internal Server Error")
    },
    description="Paye commande",
    summary="Paye commande",
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
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
def paye_room(request, idCommande):
    data = request.data
    idAdmin = request.idUser
    if 'montant' in data:
        montant = data['montant']
        try:
            commande = CommandeRoom.objects.get(idCommande=idCommande)
            if commande.idStatus_id != 1:
                return api_response(data=None, message="Commande not reserved", success=False, status_code=400)
            if commande.payed >= commande.total:
                return api_response(data=None, message="Commande already payed", success=False, status_code=400)
            if commande.payed == 0:
                commande.payed = montant
            else:
                diffAmount = commande.total - commande.payed
                if montant > diffAmount:
                    return api_response(data=None, message="The amount is greater than the remaining amount", success=False, status_code=400)
                commande.payed += montant
            if commande.payed == commande.total:
                commande.idStatus_id = 3
                message = "Confirmed Commande : " + str(montant)
            else:
                message = "Payed Commande : " + str(montant)
            commande.save()
            try:
                admin = User.objects.get(idUser=idAdmin)
                create_history(admin, 1, commande, message)
            except User.DoesNotExist:
                return api_response(data=None, message="Admin not found", success=False, status_code=404)
            delete_cache_by_prefix("commande-")
            list_cached_keys_by_prefix("commande-")
            delete_cache_by_prefix("commande-")
            return api_response(data=CommandeRoomSerializer(commande).data, message="Commande payed", success=True, status_code=200)
        except CommandeRoom.DoesNotExist:
            return api_response(data=None, message="Commande not found", success=False, status_code=404)
    else:
        return api_response(data=None, message="Invalid data", success=False, status_code=400)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Commande truncated successfully"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Truncate all commandes",
    summary="Truncate commandes",
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
def truncate(request):
    try:
        with transaction.atomic():
            CommandeRoom.objects.all().update(
                idRoom=None, idClient=None, idAdmin=None, idStatus=None
            )
            CommandeRoom.objects.all().delete()
        delete_cache_by_prefix('commande-')
        delete_cache_by_prefix('room-')
        return api_response(data=None, message="Commande truncated successfully", success=True, status_code=200)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

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
def commande(request):
    data = request.data
    dto = CreateCommandeDTO(data=data)
    if dto.is_valid():
        validated_data = dto.validated_data
        idAdmin = request.idUser
        try:
            room = Room.objects.get(idRoom=validated_data['idRoom'])
        except Room.DoesNotExist:
            return api_response(data=None, message="Room not found here", success=False, status_code=404)

        overlapping_commandes = CommandeRoom.objects.filter(
            idRoom=room,
            DateStart__lt=validated_data['DateEnd'],
            DateEnd__gt=validated_data['DateStart']
        )
        if overlapping_commandes.exists():
            return api_response(data=None, message="Room is already booked during this period", success=False, status_code=409)

        with transaction.atomic():
            price = room.price
            diffDays = int((validated_data['DateEnd'] - validated_data['DateStart']).days)
            diffDays = max(1, diffDays + 1)
            total = price * diffDays
            commande_data = {
                'idRoom_id': validated_data['idRoom'],
                'idClient_id': validated_data['idClient'],
                'idAdmin_id': idAdmin,
                'idStatus_id': validated_data['idStatus'],
                'DateStart': validated_data['DateStart'],
                'DateEnd': validated_data['DateEnd'],
                'price': price,
                'total': total,
            }
            if validated_data['idStatus'] == 3:
                commande_data['payed'] = total
            commande = CommandeRoom.objects.create(**commande_data)
            try:
                admin = User.objects.get(idUser=idAdmin)
                if validated_data['idStatus'] == 3:
                    create_history(admin, 1, commande, "Commande created")
                    create_history_room(validated_data['idRoom'], idAdmin, "Commande created")
                elif validated_data['idStatus'] == 1:
                    create_history(admin, 1, commande, "Commande reserved")
                    create_history_room(validated_data['idRoom'], idAdmin, "Commande reserved")
                elif validated_data['idStatus'] == 2:
                    create_history(admin, 1, commande, "Commande canceled")
                    create_history_room(validated_data['idRoom'], idAdmin, "Commande canceled")
                elif validated_data['idStatus'] == 4:
                    create_history(admin, 1, commande, "Commande pending")
                    create_history_room(validated_data['idRoom'], idAdmin, "Commande pending")
            except User.DoesNotExist:
                return api_response(data=None, message="Admin not found", success=False, status_code=404)
        serializer = CommandeRoomSerializer(commande)
        delete_cache_by_prefix("commande-")
        delete_cache_by_prefix("room-")
        delete_cache_by_prefix("room-stat")
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
            try:
                room = Room.objects.get(idRoom=validated_data['idRoom'])
            except Room.DoesNotExist:
                return api_response(data=None, message="Room not found here", success=False, status_code=404)
            overlapping_commandes = CommandeRoom.objects.filter(
                idRoom=room,
                DateStart__lt=validated_data['DateEnd'],
                DateEnd__gt=validated_data['DateStart']
            )
            if overlapping_commandes.exists():
                return api_response(data=None, message="Room is already booked during this period", success=False, status_code=409)

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
            create_history_room(validated_data['idRoom'], idUser, "Commande reserved")
            list_cached_keys_by_prefix("commande-")
            delete_cache_by_prefix("commande-")
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
def confirmeCommande(request, idCommande):
    try:
        idUser = request.idUser
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
        create_history_room(commande.idRoom_id, idUser, "Commande reserved")
        list_cached_keys_by_prefix("commande-")
        delete_cache_by_prefix("commande-")
        return api_response(data=serializer.data, message="Commande confirmed successfully", success=True, status_code=200)
    except CommandeRoom.DoesNotExist:
        return api_response(data=None, message="Commande not found", success=False, status_code=404)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Commande received successfully"),
        400: OpenApiResponse(description="Commande already received"),
        404: OpenApiResponse(description="Commande not found"),
    },
    description="Receive a commande by ID",
    summary="Receive commande",
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
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@token_required
@checkAdmin
@checkUser
def received_command(request, idCommande):
    try:
        commande = CommandeRoom.objects.get(idCommande=idCommande)
        if commande.received:
            return api_response(data=None, message="Commande already received", success=False, status_code=400)
        commande.received = True
        commande.dateReceived = now()
        commande.save()
        serializer = CommandeRoomSerializer(commande)
        return api_response(data=serializer.data, message="Commande received successfully", success=True, status_code=200)
    except CommandeRoom.DoesNotExist:
        return api_response(data=None, message="Commande not found", success=False, status_code=404)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="All commandes not received"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get all commandes not received",
    summary="Get all commandes not received",
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
def get_commande_not_received(request):
    try:
        cache_key = generate_cache_key('commande-not-received')
        cached_data = get_cached_data(cache_key)
        if cached_data:
            return api_response(data=cached_data, message="Commande not-received", success=True, status_code=200)
        commande = CommandeRoom.objects.filter(received=False)
        # commande = CommandeRoom.objects.filter(received=False).only('idRoom', 'price', 'total', 'payed')
        serializer = CommandeRoomSerializer(commande, many=True)
        set_cached_data(cache_key, serializer.data, timeout=settings.CACHE_TTL)
        return api_response(data=serializer.data, message="Commande not-received", success=True, status_code=200)
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
def get_commande(request):
    try:
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        cache_key = generate_cache_key('commande-allwithpaginate', page=page, limit=limit)
        cached_data = get_cached_data(cache_key)
        if cached_data:
            return api_response(data=cached_data, message="All commande room", success=True, status_code=200)

        commande = CommandeRoom.objects.select_related(
            'idRoom', 'idClient', 'idAdmin', 'idStatus'
        ).all()
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
        set_cached_data(cache_key, data_paginated, timeout=settings.CACHE_TTL)
        return api_response(data=data_paginated, message="All commande room", success=True, status_code=200)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="All commande reserved room"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get all commandes reserved room with paginate data",
    summary="Get all commandes reserved room",
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
def get_commande_reserved(request):
    try:
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        cache_key = generate_cache_key('commande-reserved', page=page, limit=limit)
        cached_data = get_cached_data(cache_key)
        if cached_data:
            return api_response(data=cached_data, message="All commande reserved room", success=True, status_code=200)

        commande = CommandeRoom.objects.filter(idStatus=1)
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
        set_cached_data(cache_key, data_paginated, timeout=settings.CACHE_TTL)
        return api_response(data=data_paginated, message="All commande reserved room", success=True, status_code=200)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)


@extend_schema(
    responses={
        200: OpenApiResponse(description="Commande status room"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get all commandes by status",
    summary="Get all commandes by status",
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
def get_commande_status(request, idStatus):
    try:
        if idStatus not in [1, 2, 3, 4]:
            return api_response(data=None, message="Invalid status", success=False, status_code=400)
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        cache_key = generate_cache_key('commande-status', page=page, idStatus=idStatus, limit=limit)
        cached_data = get_cached_data(cache_key)
        if cached_data:
            return api_response(data=cached_data, message="All commande status room", success=True, status_code=200)

        commande = CommandeRoom.objects.filter(idStatus=idStatus)
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
        set_cached_data(cache_key, data_paginated, timeout=settings.CACHE_TTL)
        return api_response(data=data_paginated, message="All commande status room", success=True, status_code=200)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="All commande search room"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Search commandes by parameters",
    summary="Search commandes",
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
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
def search_commande_client(request, idStatus):
    if idStatus not in [1, 2, 3, 4]:
        return api_response(data=None, message="Invalid status", success=False, status_code=400)
    data = request.data
    if 'query' in data:
        try:
            query = data["query"]
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 10))
            cache_key = generate_cache_key('commande-search-with-status', query=query, page=page, limit=limit, idStatus=idStatus)
            cached_data = get_cached_data(cache_key)
            if cached_data:
                return api_response(data=cached_data, message="All commande search room", success=True, status_code=200)

            commande = CommandeRoom.objects.filter(
                Q(idStatus__idStatus=idStatus) &
                (
                    Q(idClient__firstName__icontains=query) |
                    Q(idClient__name__icontains=query) |
                    Q(idClient__email__icontains=query) |
                    Q(idClient__phone__icontains=query)
                )
            )
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
            set_cached_data(cache_key, data_paginated, timeout=settings.CACHE_TTL)
            return api_response(data=data_paginated, message="All commande search room", success=True, status_code=200)
        except Exception as e:
            return api_response(data=None, message=str(e), success=False, status_code=500)
    else:
        return api_response(data=None, message="Missing query parameter", success=False, status_code=400)

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
def get_all_commande(request):
    try:
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        cache_key = generate_cache_key('commande-all', page=page, limit=limit)
        cached_data = get_cached_data(cache_key)
        if cached_data:
            return api_response(data=cached_data, message="All commande room", success=True, status_code=200)

        commande = CommandeRoom.objects.filter(idStatus_id=3)
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
        set_cached_data(cache_key, data_paginated, timeout=settings.CACHE_TTL)
        return api_response(data=data_paginated, message="All commande room", success=True, status_code=200)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="All client commande room"),
        404: OpenApiResponse(description="Client not found"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get all client commandes room",
    summary="Get all client commandes",
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
def get_all_client_commande(request, idClient):
    try:
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        cache_key = generate_cache_key('commande-all-client', idClient=idClient, page=page, limit=limit)
        cached_data = get_cached_data(cache_key)
        if cached_data:
            return api_response(data=cached_data, message="All client commande room", success=True, status_code=200)
        try:
            client = Client.objects.get(idClient=idClient)
        except Client.DoesNotExist:
            return api_response(data=None, message="Client not found", success=False, status_code=404)

        commande = CommandeRoom.objects.filter(idClient=client)
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
        set_cached_data(cache_key, data_paginated, timeout=settings.CACHE_TTL)
        return api_response(data=data_paginated, message="All client commande room", success=True, status_code=200)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="All commandes room with id"),
        404: OpenApiResponse(description="Room not found"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get all commandes room with id",
    summary="Get all commandes room with id",
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
def get_all_commande_room(request, idRoom):
    try:
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        cache_key = generate_cache_key('commande-all-room-by-id', idRoom=idRoom, page=page, limit=limit)
        cached_data = get_cached_data(cache_key)
        if cached_data:
            return api_response(data=cached_data, message="All commande room with id", success=True, status_code=200)
        try:
            room = Room.objects.get(idRoom=idRoom)
        except Room.DoesNotExist:
            return api_response(data=None, message="Room not found", success=False, status_code=404)
        commande = CommandeRoom.objects.filter(idRoom=room, idStatus_id=3)
        serializer = CommandeRoomSerializer(commande, many=True)
        data_paginated = {
            'commande': serializer.data,
            'paginations': {
                'document': len(serializer.data),
                'total_pages': page,
                'current_page': page,
                'limit': limit
            }
        }
        set_cached_data(cache_key, data_paginated, timeout=settings.CACHE_TTL)
        return api_response(data=data_paginated, message="All commande room with id", success=True, status_code=200)
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
def get_commande_by_id(request, idCommande):
    try:
        cache_key = generate_cache_key('commande-ById', idCommande=idCommande)
        cached_data = get_cached_data(cache_key)
        if cached_data:
            return api_response(data=cached_data, message="Commande retrieved successfully", success=True, status_code=200)
        commande = CommandeRoom.objects.get(idCommande=idCommande)
        serializer = CommandeRoomSerializer(commande)
        set_cached_data(cache_key, serializer.data, timeout=settings.CACHE_TTL)
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
            idUser = request.idUser
            idRoom = room.idRoom
            create_history_room(idRoom, idUser, "Room created")
            list_cached_keys_by_prefix("room-")
            delete_cache_by_prefix("room-")
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
        idUser = request.idUser
        create_history_room(idRoom, idUser, "Room images uploaded")
        list_cached_keys_by_prefix("room-")
        delete_cache_by_prefix("room-")
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
        idUser = request.idUser
        create_history_room(image.idRoom, idUser, "Room image deleted")
        list_cached_keys_by_prefix("room-")
        delete_cache_by_prefix("room-")
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
        list_cached_keys_by_prefix("room-")
        delete_cache_by_prefix("room-")
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
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))

        cache_key = generate_cache_key('room-allwithpaginate', page=page, limit=limit)
        cached_data = get_cached_data(cache_key)
        if cached_data:
            return api_response(data=cached_data, message="All rooms from caches", success=True, status_code=200)

        rooms = Room.objects.all().select_related('idAdmin')
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
        set_cached_data(cache_key, data_paginated, timeout=settings.CACHE_TTL)
        return api_response(data=data_paginated, message="All rooms", success=True, status_code=200)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Client for this room"),
        404: OpenApiResponse(description="Room not found"),
        404: OpenApiResponse(description="Room is available"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get client for this room",
    summary="Get client for this room",
    parameters=[
        OpenApiParameter(
            name='idRoom',
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
def get_client_room_not_available(request, idRoom):
    try:
        cache_key = generate_cache_key('room-client-unavailable', idRoom=idRoom)
        cached_data = get_cached_data(cache_key)
        if cached_data:
            return api_response(data=cached_data, message="Client for this room", success=True, status_code=200)
        room = Room.objects.get(idRoom=idRoom)
        if room.available:
            return api_response(data=None, message="Room is available", success=False, status_code=400)
        today = now().date()
        try:
            commandes = CommandeRoom.objects.filter(
                idRoom=room,
                DateStart__lte=today,
                DateEnd__gte=today
            )
            commandes_data = [
                {
                    "Client": ClientSerializer(commande.idClient).data,
                    "Commande": CommandeRoomSerializer(commande).data
                }
                for commande in commandes
            ]
            set_cached_data(cache_key, commandes_data, timeout=settings.CACHE_TTL)
            return api_response(data=commandes_data, message="Client for this room", success=True, status_code=200)
        except CommandeRoom.DoesNotExist:
            return api_response(data=None, message="Commande not found", success=False, status_code=404)
    except Room.DoesNotExist:
        return api_response(data=None, message="Room not found", success=False, status_code=404)

@extend_schema(
    responses={
        200: OpenApiResponse(description="Deleted rooms"),
        500: OpenApiResponse(description="Internal server error")
    },
    description="Get all deleted rooms",
    summary="Get deleted rooms",
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
def deleted(request):
    try:
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))

        cache_key = generate_cache_key('room-deleted', page=page, limit=limit)
        cached_data = get_cached_data(cache_key)
        if cached_data:
            return api_response(data=cached_data, message="Deleted rooms", success=True, status_code=200)
        deleted_rooms = Room.all_objects.filter(deletedAt__isnull=False)
        paginator = Paginator(deleted_rooms, limit)
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
        set_cached_data(cache_key, data_paginated, timeout=settings.CACHE_TTL)
        return api_response(data=data_paginated, message="Deleted rooms", success=True, status_code=200)
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
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))

        cache_key = generate_cache_key('room-image-allwithpaginate', page=page, limit=limit)
        cache_data = get_cached_data(cache_key)
        if cache_data:
            return api_response(data=cache_data, message="All images", success=True, status_code=200)

        imageRoom = RoomImage.objects.all()
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
        set_cached_data(cache_key, data_paginated, timeout=settings.CACHE_TTL)
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
        cache_key = generate_cache_key('room-get-image', idRoom=idRoom)
        cache_data = get_cached_data(cache_key)
        if cache_data:
            return api_response(data=cache_data, message="All images for a room", success=True, status_code=200)
        try:
            room = Room.objects.get(idRoom=idRoom)
        except Room.DoesNotExist:
            return api_response(data=None, message="Room not found", success=False, status_code=404)
        imageRoom = RoomImage.objects.filter(idRoom=idRoom)
        serializer = RoomImageSerializer(imageRoom, many=True)
        set_cached_data(cache_key, serializer.data, timeout=settings.CACHE_TTL)
        return api_response(data=serializer.data, message="All images for a room", success=True, status_code=200)
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
        cache_key = generate_cache_key('room-detail', idRoom=idRoom)
        cache_data = get_cached_data(cache_key)
        if cache_data:
            return api_response(data=cache_data, message="Room retrieved successfully from caches", success=True, status_code=200)
        room = Room.objects.get(idRoom=idRoom)
        serializer = RoomResponseSerializer(room)
        imageRome = RoomImage.objects.filter(idRoom=idRoom)
        serializerRoom = RoomImageSerializer(imageRome, many=True)
        data = {
            'Room': serializer.data,
            'images': serializerRoom.data
        }
        set_cached_data(cache_key, data, timeout=settings.CACHE_TTL)
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
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))

        cache_key = generate_cache_key('room-unavailable', page=page, limit=limit)
        cache_data = get_cached_data(cache_key)
        if cache_data:
            return api_response(data=cache_data, message="Rooms unavailable retrieved successfully", success=True, status_code=200)

        rooms = Room.objects.filter(available=False)
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
        set_cached_data(cache_key, data_paginated, timeout=settings.CACHE_TTL)
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
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        cache_key = generate_cache_key('room-available', page=page, limit=limit)
        cache_data = get_cached_data(cache_key)
        if cache_data:
            return api_response(data=cache_data, message="Rooms available retrieved successfully", success=True, status_code=200)

        rooms = Room.objects.filter(available=True)
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
        set_cached_data(cache_key, data_paginated, timeout=settings.CACHE_TTL)
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
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))

        cache_key = generate_cache_key('room-search', query=query, page=page, limit=limit)
        cache_data = get_cached_data(cache_key)
        if cache_data:
            return api_response(data=cache_data, message="Rooms search retrieved successfully", success=True, status_code=200)

        rooms = Room.objects.filter(
            Q(title__icontains=query) |
            Q(subTitle__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query)
        )

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
        set_cached_data(cache_key, data_paginated, timeout=settings.CACHE_TTL)
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

            idUser = request.idUser
            create_history_room(room.idRoom, idUser, "Room updated")

            list_cached_keys_by_prefix("room-")
            delete_cache_by_prefix("room-")
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
def free_room(request, idRoom):
    try:
        room = Room.objects.get(idRoom=idRoom)
        room.available = True
        room.dateAvailable = None
        room.save()

        idUser = request.idUser
        create_history_room(room.idRoom, idUser, "Room freed")

        list_cached_keys_by_prefix("room-")
        delete_cache_by_prefix("room-")
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
        create_history_room(room.idRoom, currentUser, "Room deleted")
        room.save()
        list_cached_keys_by_prefix("room-")
        delete_cache_by_prefix("room-")
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
        create_history_room(room.idRoom, currentUser, "Room recovered")
        list_cached_keys_by_prefix("room-")
        delete_cache_by_prefix("room-")
        return api_response(data=None, message="Room recovered successfully", success=True, status_code=200)
    except Room.DoesNotExist:
        return api_response(data=None, message="Room not found", success=False, status_code=404)
    except Exception as e:
        return api_response(data=None, message=str(e), success=False, status_code=500)