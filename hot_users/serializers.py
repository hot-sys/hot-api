from rest_framework import serializers
from .models import Role, User, UserPreference
from utils.api_response import api_response

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = 'idRole', 'poste'

    def validate_poste(self, value):
        if Role.objects.filter(poste=value).exists():
            raise serializers.ValidationError("Role with poste already exists.")
        return value

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = 'idPreference', 'idUser', 'theme', 'color'

class UserSerializer(serializers.ModelSerializer):
    preference = UserPreferenceSerializer()
    idRole = RoleSerializer()
    class Meta:
        model = User
        fields = 'idUser', 'idRole', 'login', 'password', 'name', 'firstname', 'phone', 'email', 'genre', 'adress', 'createdAt', 'updatedAt', 'deletedAt', 'preference'

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'idUser', 'idRole', 'login', 'password', 'name', 'firstname', 'phone', 'email', 'genre', 'adress', 'createdAt', 'updatedAt', 'deletedAt'

class UserSerializerResponse(serializers.ModelSerializer):
    preference = UserPreferenceSerializer(read_only=True)
    idRole = RoleSerializer(read_only=True)
    class Meta:
        model = User
        fields = 'idUser', 'idRole', 'login', 'image', 'name', 'firstname', 'phone', 'email', 'genre', 'adress', 'createdAt', 'preference'

class UpdatePosteDTO(serializers.Serializer):
    idRole = serializers.IntegerField(required=True)
    def validate_idRole(self, value):
        try:
            return Role.objects.get(idRole=value)
        except Role.DoesNotExist:
            raise serializers.ValidationError("Role not found")

    def validate(self, data):
        if len(data) != 1 or "idRole" not in data:
            raise serializers.ValidationError("Only one field is allowed in the request.")
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
            raise serializers.ValidationError("Role not found")
        return value
    def checkLogin(self, value):
        if User.objects.filter(login=value).exists():
            raise serializers.ValidationError("Login already exists.")
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
            raise serializers.ValidationError("Role with poste already exists.")
        return value