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

class UpdatePosteDTO(serializers.Serializer):
    idRole = serializers.IntegerField(required=True)
    def validate_idRole(self, value):
        try:
            return Role.objects.get(idRole=value)
        except Role.DoesNotExist:
            raise serializers.ValidationError("Role not found")

    def validate(self, data):
        if len(data) != 1 or "idRole" not in data:
            return api_response(message="Only 'idRole' is allowed in the request.", success=False, status_code=400)
        return data

class LoginDTO(serializers.Serializer):
    login = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)

class RegisterDTO(serializers.Serializer):
    idRole = serializers.IntegerField(required=True)
    login = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, min_length=8, required=True)
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
    def checkLogin(self, value):
        if User.objects.filter(login=value).exists():
            return api_response(message="Login already exists.", success=False, status_code=400)
        return value
    def checkEmail(self, value):
        if User.objects.filter(email=value).exists():
            return api_response(message="Email already exists.", success=False, status_code=400)
        return value

class UpdateUserDto(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    firstname = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True, allow_null=True)
    genre = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    adress = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    password = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)

class RoleDTO(serializers.Serializer):
    poste = serializers.CharField(max_length=255, required=True)
    def validate_poste(self, value):
        if Role.objects.filter(poste=value).exists():
            return api_response(message="Role with poste already exists.", success=False, status_code=400)
        return value