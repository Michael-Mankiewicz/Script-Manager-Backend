from rest_framework import serializers
from .models import Script

class AddressChangeSerializer(serializers.Serializer):
    cartonfile = serializers.FileField()
    fedexinvoice = serializers.FileField()

class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ['id', 'name', 'description']