from rest_framework import serializers
from .models import Entite

class EntiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entite
        fields = '__all__'
