from rest_framework import serializers
from .models import Status, Service, ServiceItem, CommandeService
from hot_clients.models import Client
from hot_users.models import User
from hot_clients.serializers import ClientSerializer
from hot_users.serializers import UserSerializerResponse

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def validate_name(self, value):
        if Service.objects.filter(name=value).exists():
            raise serializers.ValidationError("Service already exists")
        return value

class ServiceItemSerializer(serializers.ModelSerializer):
    idService = ServiceSerializer()
    class Meta:
        model = ServiceItem
        fields = 'idService', 'title', 'subTitle', 'description', 'price', 'unity', 'createdAt'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

    def validate_name(self, value):
        if Status.objects.filter(name=value).exists():
            raise serializers.ValidationError("Status already exists")
        return value

class CommandeServiceSerializer(serializers.ModelSerializer):
    idItem = ServiceItemSerializer()
    idClient = ClientSerializer()
    idStatus = StatusSerializer()
    idAdmin = UserSerializerResponse()
    class Meta:
        model = CommandeService
        fields = 'idItem', 'idClient', 'idStatus', 'idAdmin', 'number', 'total', 'createdAt'

class CreateServiceDTO(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=255, required=False)

    def validate_name(self, value):
        if Service.objects.filter(name=value).exists():
            raise serializers.ValidationError("Service already exists")
        return value

class CreateServiceItemDTO(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=True)
    subTitle = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(max_length=255, required=False)
    price = serializers.FloatField(required=True)
    unity = serializers.CharField(max_length=255, required=True)

    def validate_idService(self, value):
        if not Service.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Service does not exist")
        return value

    def validate_title(self, value):
        if ServiceItem.objects.filter(title=value).exists():
            raise serializers.ValidationError("Service item already exists")
        return value

class UpdateServiceItemDTO(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)
    subTitle = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(max_length=255, required=False)
    price = serializers.FloatField(required=False)
    unity = serializers.CharField(max_length=255, required=False)

    def validate_idItem(self, value):
        if not ServiceItem.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Service item does not exist")
        return value

    def validate_title(self, value):
        if ServiceItem.objects.filter(title=value).exists():
            raise serializers.ValidationError("Service item already exists")
        return value

class CreateCommandeServiceDTO(serializers.Serializer):
    idItem = serializers.IntegerField(required=True)
    idClient = serializers.IntegerField(required=True)
    idStatus = serializers.IntegerField(required=True)
    number = serializers.IntegerField(required=True)

    def validate_idItem(self, value):
        if not ServiceItem.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Service item does not exist")
        return value

    def validate_idClient(self, value):
        if not Client.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Client does not exist")
        return value

    def validate_idStatus(self, value):
        if not Status.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Status does not exist")
        return value

    def validate_idAdmin(self, value):
        if value is not None and not User.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Admin does not exist")
        return value