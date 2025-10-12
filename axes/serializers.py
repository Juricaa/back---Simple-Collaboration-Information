from rest_framework import serializers

from objectifs.models import Objectif
from .models import Axe

class ObjectifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objectif
        fields = ['id_objectif', 'id_axe', 'intitule', 'type', 'description']

class AxeSerializer(serializers.ModelSerializer):
    objectifs = ObjectifSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Axe
        fields = [
            'id_axe', 'id_utilisateur', 'titre', 'description',
            'annee', 'statut', 'objectifs'
        ]

    def create(self, validated_data):
        # Extraire les objectifs
        objectifs_data = validated_data.pop('objectifs', [])

        # Créer l'axe
        axe = Axe.objects.create(**validated_data)

        # Créer les objectifs associés
        for obj_data in objectifs_data:
            Objectif.objects.create(id_axe=axe, **obj_data)

        return axe


# class AxeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Axe
#         fields = '__all__'
