from rest_framework import serializers
from .models import Room
from hot_users.models import User
from hot_users.serializers import UserSerializerResponse
from utils.api_response import api_response
from django.utils import timezone


class RoomSerializer(serializers.ModelSerializer):
    idAdmin = UserSerializerResponse(read_only=True)
    class Meta:
        model = Room
        fields = 'idRoom', 'idAdmin', 'title', 'subTitle', 'description', 'price', 'available', 'dateAvailable', 'info'


class CreateRoomDTO(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=True)
    subTitle = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(required=True)
    price = serializers.IntegerField(required=True)
    available = serializers.BooleanField(required=True)
    dateAvailable = serializers.DateTimeField(required=False)
    info = serializers.JSONField(required=False)

    def validate_idAdmin(self, value):
        try:
            user = User.objects.get(idUser=value)
            if UserSerializerResponse(user).data['idRole'] != 1:
                raise serializers.ValidationError("Only admin users can create a room.")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

    def validate_title(self, value):
        if Room.objects.filter(title=value).exists():
            raise serializers.ValidationError("Title already exists")
        return value

    def validate_dateAvailable(self, value):
        if value is not None and value < timezone.now():
            raise serializers.ValidationError("Date available must be greater than the current date")
        return value