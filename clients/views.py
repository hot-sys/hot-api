from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import UserClient, ActivateAccount
from .serializers import UserClientSerializerReturn, UserClientRegisterSerializer, UserClientSerializer
from django.urls import reverse
from mail.email_utils import sendMail
from .utils import generate_token, jwt_required
import os
from dotenv import load_dotenv
load_dotenv()

@api_view(['POST'])
def register(request):
    serializer = UserClientRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = UserClient(
            email=serializer.validated_data['email'],
            last_name=serializer.validated_data['last_name'],
            first_name=serializer.validated_data['first_name'],
            phone=serializer.validated_data['phone'],
            position_lat=serializer.validated_data['position_lat'],
            position_long=serializer.validated_data['position_long'],
            validation_client=False  
        )
        
        password = serializer.validated_data['password_client']
        user.set_password(password)
        
        user.save()  
        
        activation = ActivateAccount.objects.create(email=user.email)
        
        activation_link = f"{os.getenv('SERVEUR')}/api/clients/activate/{user.email}"
        
        email_content = f'Click this link to activate your account: {activation_link}'

        sendMail(user.email, 'Activate your account', email_content)
        
        return JsonResponse({'message': 'User registered successfully. Check your email to activate your account.'}, status=status.HTTP_201_CREATED)
    return JsonResponse({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = UserClient.objects.get(email=email)
    except UserClient.DoesNotExist:
        return JsonResponse({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    if user.check_password(password):
        user.status_client = True
        user.save()
        
        # GENERATE TOKEN
        serializer = UserClientSerializerReturn(user)
        token = generate_token(UserClientSerializer(user).data["id"])
        return JsonResponse({
            'message': 'Login successful',
            'user': serializer.data,
            'access_token': token,
        })
    else:
        return JsonResponse({'error': 'Invalid Credentials with passwrod'}, status=status.HTTP_401_UNAUTHORIZED)

@jwt_required
@api_view(['POST'])
def logout(request):
    currrentUser = request.user_object
    user = currrentUser
    user.status_client = False
    user.save()
    return JsonResponse({'message': 'Logout successful'}, status=status.HTTP_204_NO_CONTENT)

@jwt_required
@api_view(['GET'])
def user_detail(request):
    currrentUser = request.user_actif
    return JsonResponse(currrentUser, safe=False)
    
@api_view(['GET'])
def user_list(request):
    users = UserClient.objects.all()
    serializer = UserClientSerializerReturn(users, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def activate_account(request, email):
    activation = get_object_or_404(ActivateAccount, email=email)
    if activation.expires_at < timezone.now():
        return JsonResponse({'error': 'Activation link has expired.'}, status=status.HTTP_400_BAD_REQUEST, safe=False)
    user = get_object_or_404(UserClient, email=email)
    user.validation_client = True
    user.save()
    activation.delete()
    return JsonResponse({'message': 'Account activated successfully.'}, status=status.HTTP_200_OK, safe=False)

