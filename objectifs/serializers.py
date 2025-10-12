from rest_framework import serializers
from .models import Objectif

class ObjectifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objectif
        fields = '__all__'
