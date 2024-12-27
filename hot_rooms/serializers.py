from rest_framework import serializers
from .models import Room, RoomImage, CommandeRoom
from hot_users.models import User
from hot_users.serializers import UserSerializerResponse
from hot_services.serializers import StatusSerializer
from hot_clients.serializers import ClientSerializer
from hot_services.models import Status
from utils.api_response import api_response
from django.utils import timezone

class RoomSerializer(serializers.ModelSerializer):
    idAdmin = UserSerializerResponse(read_only=True)
    class Meta:
        model = Room
        fields = 'idRoom', 'idAdmin', 'title', 'subTitle', 'description', 'price', 'available', 'dateAvailable', 'info'

class RoomResponseSerializer(serializers.ModelSerializer):
    idAdmin = UserSerializerResponse(read_only=True)
    class Meta:
        model = Room
        fields = 'idRoom', 'idAdmin', 'title', 'subTitle', 'description', 'price', 'available', 'dateAvailable', 'info', 'createdAt', 'updatedAt'

class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ('idImage', 'idRoom', 'image', 'uploaded_at')

class CommandeRoomSerializer(serializers.ModelSerializer):
    idRoom = RoomResponseSerializer(read_only=True)
    idClient = ClientSerializer(read_only=True)
    idAdmin = UserSerializerResponse(read_only=True)
    idStatus = StatusSerializer(read_only=True)
    class Meta:
        model = CommandeRoom
        fields = 'idCommande', 'idRoom', 'idClient', 'idAdmin', 'idStatus', 'DateStart', 'DateEnd', 'price', 'total', 'createdAt'

class CreateCommandeDTO(serializers.Serializer):
    idRoom = serializers.IntegerField(required=True)
    idClient = serializers.IntegerField(required=False)
    idStatus = serializers.IntegerField(required=False)
    DateStart = serializers.DateTimeField(required=True)
    DateEnd = serializers.DateTimeField(required=True)

    def validate_idRoom(self, value):
        if not Room.objects.filter(idRoom=value).exists():
            raise serializers.ValidationError("Room not found")
        if Room.objects.get(idRoom=value).available == False:
            raise serializers.ValidationError("Room not available")
        return value

    def validate_idClient(self, value):
        if not User.objects.filter(idUser=value).exists():
            raise serializers.ValidationError("Client not found")
        return value

    def validate_idStatus(self, value):
        if not Status.objects.filter(idStatus=value).exists():
            raise serializers.ValidationError("Status not found")
        return value

    # def validate_DateStart(self, value):
    #     if value <= timezone.now():
    #         raise serializers.ValidationError("Date start must be greater than the current date")
    #     return value

    # def validate_DateEnd(self, value):
    #     if value < timezone.now():
    #         raise serializers.ValidationError("Date end must be greater than the current date")
    #     return value

    def check_date(self, start, end):
        if start > end:
            raise serializers.ValidationError("Date start must be less than date end")
    def check_if_date_exist_in_commande(self, idRoom, start, end):
        if CommandeRoom.objects.filter(idRoom=idRoom, DateStart__lte=start, DateEnd__gte=start).exists() or CommandeRoom.objects.filter(idRoom=idRoom, DateStart__lte=end, DateEnd__gte=end).exists():
            raise serializers.ValidationError("Room already booked for this period")
        if CommandeRoom.objects.filter(idRoom=idRoom, DateStart__gte=start, DateEnd__lte=end).exists():
            raise serializers.ValidationError("Room already booked for this period")

class CreateRoomDTO(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=True)
    subTitle = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(required=True)
    price = serializers.IntegerField(min_value=0, max_value=1000000, required=True)
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

class UpdateRoomDTO(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)
    subTitle = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(required=False)
    price = serializers.IntegerField(required=False)
    available = serializers.BooleanField(required=False)
    dateAvailable = serializers.DateTimeField(required=False)
    info = serializers.JSONField(required=False)

    def validate_title(self, value):
        if Room.objects.filter(title=value).exists():
            raise serializers.ValidationError("Title already exists")
        return value

    def validate_dateAvailable(self, value):
        if value is not None and value < timezone.now():
            raise serializers.ValidationError("Date available must be greater than the current date")
        return value