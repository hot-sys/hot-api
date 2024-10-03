from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Reservation
from .serializers import ReservationSerializer

@api_view(['POST'])
def create_reservation(request):
    serializer = ReservationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(['GET'])
def reservation_detail(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    serializer = ReservationSerializer(reservation)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def reservation_list(request):
    reservations = Reservation.objects.all()
    serializer = ReservationSerializer(reservations, many=True)
    return JsonResponse(serializer.data, safe=False)
