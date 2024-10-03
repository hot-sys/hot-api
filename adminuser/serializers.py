from rest_framework import serializers
from .models import UserAdmin

class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdmin
        fields = '__all__'

class UserAdminSerializerReturn(serializers.ModelSerializer):
    class Meta:
        model = UserAdmin
        fields = [
            'id', 'login', 'poste', 'status', 'name',
            'first_name', 'email', 'phone', 'address', 'photo'
        ]
