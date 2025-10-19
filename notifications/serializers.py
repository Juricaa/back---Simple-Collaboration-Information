from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id_notification',
            'id_utilisateur',
            'titre',
            'message',
            'type',
            'id_cible',
            'date_creation',
            'est_lu',
            'role_cible',
        ]
        read_only_fields = ['id_notification', 'date_creation']