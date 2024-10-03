from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Activite, TypeActivite
from .serializers import ActiviteSerializer, TypeActiviteSerializer

@api_view(['POST'])
def create_activity(request):
    serializer = ActiviteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(['GET'])
def activity_detail(request, id):
    activity = get_object_or_404(Activite, id=id)
    serializer = ActiviteSerializer(activity)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def activity_list(request):
    activities = Activite.objects.all()
    serializer = ActiviteSerializer(activities, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def type_activity_list(request):
    types = TypeActivite.objects.all()
    serializer = TypeActiviteSerializer(types, many=True)
    return JsonResponse(serializer.data, safe=False)
