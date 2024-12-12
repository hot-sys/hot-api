from rest_framework.response import Response
from rest_framework import status

def api_response(data=None, message="Success", success=True, status_code=status.HTTP_200_OK):
    return Response({
        "success": success,
        "code": status_code,
        "message": message,
        "data": data
    })