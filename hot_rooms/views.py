from rest_framework.decorators import api_view, authentication_classes
from utils.token_required import token_required
from utils.api_response import api_response
from rest_framework.authentication import TokenAuthentication
from hot_users.decorators.checkUser import checkUser
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter


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
    return api_response(message="All rooms", success=True, status_code=200)