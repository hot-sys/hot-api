from rest_framework import serializers
from .models import Status, Service, ServiceItem

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