from rest_framework import serializers
from .models import Status

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

    def validate_name(self, value):
        if Status.objects.filter(name=value).exists():
            raise serializers.ValidationError("Status already exists")
        return value