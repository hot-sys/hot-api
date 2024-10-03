from rest_framework import serializers
from .models import Reservation
from activity.serializers import ActiviteSerializer
from clients.serializers import UserClientSerializerReturn
from adminuser.serializers import UserAdminSerializerReturn

class ReservationSerializer(serializers.ModelSerializer):
    activite = ActiviteSerializer()
    client = UserClientSerializerReturn()
    admin = UserAdminSerializerReturn()

    class Meta:
        model = Reservation
        fields = '__all__'
