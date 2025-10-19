from django.db import models

from utilisateurs.models import Utilisateur

def generate_notification_custom_id():
    last_notification = Notification.objects.all().order_by('id_notification').last()
    if not last_notification:
        return 'N0001'
    notification_id = last_notification.id_notification
    notification_int = int(notification_id.split('N')[-1])
    new_notification_int = notification_int + 1
    new_notification_id = 'N' + str(new_notification_int).zfill(4)
    return new_notification_id
  

class Notification(models.Model):
    id_notification = models.CharField(primary_key=True, max_length=10, default=generate_notification_custom_id, editable=False)
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(
    max_length=100,
    choices=[
        ('commentaire', 'Commentaire'),
        ('axe', 'Axe'),
        ('objectif', 'Objectif'),
        ('projet', 'Projet'),
        ('rapport', 'Rapport'),
        ('alerte', 'Alerte'),
    ],)
    id_cible = models.CharField(max_length=20, null=True, blank=True)  
    role_cible = models.CharField(max_length=50, null=True, blank=True) 
    date_creation = models.DateTimeField(auto_now_add=True)
    est_lu = models.BooleanField(default=False)

