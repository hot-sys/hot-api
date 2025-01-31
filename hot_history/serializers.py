from rest_framework import serializers
from .models import typeHistorique, Historique, HistoryRoom
from hot_users.models import User
from hot_rooms.models import CommandeRoom, Room
from hot_services.models import CommandeService
from hot_rooms.serializers import CommandeRoomSerializer
from hot_services.serializers import CommandeServiceSerializer
from hot_users.serializers import UserSerializerResponse
from hot_rooms.serializers import RoomResponseSerializer

class typeHistoriqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = typeHistorique
        fields = '__all__'

    def validate_name(self, value):
        if typeHistorique.objects.filter(name=value).exists():
            raise serializers.ValidationError("Type already exists")
        return value

class HistoryRoomSerializer(serializers.ModelSerializer):
    idRoom = RoomResponseSerializer()
    idAdmin = UserSerializerResponse()
    class Meta:
        model = HistoryRoom
        fields = 'idHistory', 'idRoom', 'idAdmin', 'description', 'createdAt'

class HistoriqueSerializer(serializers.ModelSerializer):
    idType = typeHistoriqueSerializer()
    idAdmin = UserSerializerResponse()
    idCommandeRoom = CommandeRoomSerializer()
    idCommandeService = CommandeServiceSerializer()
    class Meta:
        model = Historique
        fields = 'idHistorique', 'idAdmin', 'idType', 'idCommandeRoom', 'idCommandeService', 'description', 'createdAt'

class CreateHistoryRoom(serializers.Serializer):
    idRoom = serializers.IntegerField()
    idAdmin = serializers.IntegerField()
    description = serializers.CharField(required=False)

    def validate_idRoom(self, value):
        if not Room.objects.filter(idRoom=value).exists():
            raise serializers.ValidationError("Room does not exist")
        return value

    def validate_idAdmin(self, value):
        if not User.objects.filter(idUser=value).exists():
            raise serializers.ValidationError("User does not exist")
        return value

class CreateHistoriqueDTO(serializers.Serializer):
    idAdmin = serializers.IntegerField()
    idType = serializers.IntegerField()
    idCommandeRoom = serializers.IntegerField(required=False)
    idCommandeService = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)

    def validate_idAdmin(self, value):
        if not User.objects.filter(idUser=value).exists():
            raise serializers.ValidationError("User does not exist")
        return value

    def validate_idType(self, value):
        if not typeHistorique.objects.filter(idType=value).exists():
            raise serializers.ValidationError("Type does not exist")
        return value

    def validate_idCommandeRoom(self, value):
        if value is not None and not CommandeRoom.objects.filter(idCommandeRoom=value).exists():
            raise serializers.ValidationError("Commande Room does not exist")
        return value

    def validate_idCommandeService(self, value):
        if value is not None and not CommandeService.objects.filter(idCommandeService=value).exists():
            raise serializers.ValidationError("Commande Service does not exist")
        return value