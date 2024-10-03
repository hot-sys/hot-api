from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import UserAdmin
from .serializers import UserAdminSerializer
from django.contrib.auth.hashers import make_password, check_password

@api_view(['POST'])
def register(request):
    serializer = UserAdminSerializer(data=request.data)
    if serializer.is_valid():
        # Hash the password before saving
        password = request.data.get('password')
        user = serializer.save()
        user.password = make_password(password)
        user.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = UserAdmin.objects.get(email=email)
    except UserAdmin.DoesNotExist:
        return JsonResponse({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if check_password(password, user.password):
        # You can generate a token or session here if needed
        return JsonResponse({'message': 'Login successful'})
    else:
        return JsonResponse({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def user_detail(request, id):
    user = get_object_or_404(UserAdmin, id=id)
    serializer = UserAdminSerializer(user)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def user_list(request):
    users = UserAdmin.objects.all()
    serializer = UserAdminSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)
