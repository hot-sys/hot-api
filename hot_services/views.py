
from rest_framework.decorators import api_view, authentication_classes, parser_classes
from utils.token_required import token_required
from utils.api_response import api_response
from rest_framework.authentication import TokenAuthentication
from hot_users.decorators.checkUser import checkUser
from hot_users.decorators.checkAdmin import checkAdmin
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from .models import Status
from .serializers import StatusSerializer
from django.db import transaction
from datetime import datetime, timedelta



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
def create(request):
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
def update(request, idStatus):
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
def get_all(request):
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
        )
    ]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@token_required
@checkUser
@checkAdmin
def get_by_id(request, idStatus):
    try:
        status = Status.objects.get(idStatus=idStatus)
        serializer = StatusSerializer(status)
        return api_response(data=serializer.data, message="Status found", success=True, status_code=200)
    except Status.DoesNotExist:
        return api_response(message="Status not found", success=False, status_code=404)