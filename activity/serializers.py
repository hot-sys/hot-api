from rest_framework import serializers
from .models import TypeActivite, Activite
from adminuser.serializers import UserAdminSerializerReturn
from clients.serializers import UserClientSerializerReturn

class TypeActiviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeActivite
        fields = '__all__'

class ActiviteSerializer(serializers.ModelSerializer):
    type_activite = TypeActiviteSerializer() 
    client = UserClientSerializerReturn()
    admin = UserAdminSerializerReturn()
    class Meta:
        model = Activite
        fields = '__all__'
