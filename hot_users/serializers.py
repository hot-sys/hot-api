from rest_framework import serializers
from .models import Role, User, UserPreference
from utils.api_response import api_response

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = 'idRole', 'poste'

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = 'idPreference', 'idUser', 'theme', 'color'

class UserSerializer(serializers.ModelSerializer):
    preference = UserPreferenceSerializer(read_only=True)
    class Meta:
        model = User
        fields = 'idUser', 'idRole', 'login', 'password', 'name', 'firstname', 'phone', 'email', 'genre', 'adress', 'createdAt', 'updatedAt', 'deletedAt', 'preference'

class UserSerializerResponse(serializers.ModelSerializer):
    preference = UserPreferenceSerializer(read_only=True)
    class Meta:
        model = User
        fields = 'idUser', 'idRole', 'login', 'name', 'firstname', 'phone', 'email', 'genre', 'adress', 'createdAt', 'preference'

class LoginDTO(serializers.Serializer):
    login = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)

class RegisterDTO(serializers.Serializer):
    idRole = serializers.IntegerField(required=True)
    login = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)
    name = serializers.CharField(max_length=255, required=True)
    firstname = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True, allow_null=True)
    genre = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    adress = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    def validate_idRole(self, value):
        if not Role.objects.filter(idRole=value).exists():
            return api_response(message="Role not found", success=False, status_code=404)
        return value

class RoleDTO(serializers.Serializer):
    poste = serializers.CharField(max_length=255, required=True)
    def validate_poste(self, value):
        if Role.objects.filter(poste=value).exists():
            return api_response(message="Role with poste already exists.", success=False, status_code=400)
        return value