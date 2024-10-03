from rest_framework import serializers
from .models import UserClient

class UserClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClient
        fields = '__all__'

class UserClientSerializerReturn(serializers.ModelSerializer):
    class Meta:
        model = UserClient
        fields = [
            'id', 'email', 'last_name', 'first_name', 'genre', 'country',
            'address_client', 'position_lat', 'position_long', 'phone',
            'validation_client', 'status_client', 'photo'
        ]

class UserClientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClient
        fields = [
            'email', 'password_client', 'last_name', 
            'first_name', 'phone', 'position_lat', 'position_long'
        ]