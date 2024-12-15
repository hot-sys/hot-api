from rest_framework import serializers
from .models import Status, Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def validate_name(self, value):
        if Service.objects.filter(name=value).exists():
            raise serializers.ValidationError("Service already exists")
        return value
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