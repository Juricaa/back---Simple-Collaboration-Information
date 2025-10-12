from rest_framework import serializers
from .models import EntiteProjet

class EntiteProjetSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntiteProjet
        fields = '__all__'
