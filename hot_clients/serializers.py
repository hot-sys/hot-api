from  rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = 'idClient', 'name', 'firstName', 'phone', 'email', 'genre', 'adress', 'cin', 'createdAt'

class CreateClientDTO(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=True)
    firstName = serializers.CharField(max_length=255, required=True)
    phone = serializers.CharField(max_length=20, required=False)
    email = serializers.EmailField(required=True)
    genre = serializers.CharField(max_length=10, required=False)
    adress = serializers.CharField(required=False)
    cin = serializers.CharField(max_length=50, required=True)

    def validate_email(self, value):
        if Client.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_cin(self, value):
        if Client.objects.filter(cin=value).exists():
            raise serializers.ValidationError("CIN already exists")
        return value

class UpdateClientDTO(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    firstName = serializers.CharField(max_length=255, required=False)
    phone = serializers.CharField(max_length=20, required=False)
    email = serializers.EmailField(required=False)
    genre = serializers.CharField(max_length=10, required=False)
    adress = serializers.CharField(required=False)
    cin = serializers.CharField(max_length=50, required=False)

    # def validate_email(self, value):
    #     if Client.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("Email already exists")
    #     return value

    # def validate_cin(self, value):
    #     if Client.objects.filter(cin=value).exists():
    #         raise serializers.ValidationError("CIN already exists")
    #     return value