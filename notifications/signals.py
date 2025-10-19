from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from notifications.models import Notification
from rapports.models import Rapport
from commentaires.models import Commentaire
from projets.models import Projet
from utilisateurs.models import Utilisateur

@receiver(post_save, sender=Rapport)
def create_notification_on_rapport(sender, instance, created, **kwargs):
    if created:
        # Alerter les administrateurs
        admins = Utilisateur.objects.filter(role='admin')
        for admin in admins:
            Notification.objects.create(
                id_utilisateur=admin,
                titre='Nouveau rapport ajouté',
                message=f'Un nouveau rapport {instance.id_rapport} a été ajouté pour le projet {instance.id_projet.titre or instance.id_projet.id_projet}.',
                type='rapport',
                id_cible=instance.id_rapport,
                role_cible='admin'
            )
        # Notifier le propriétaire du projet si différent du créateur
        if instance.id_utilisateur != instance.id_projet.id_utilisateur:
            Notification.objects.create(
                id_utilisateur=instance.id_projet.id_utilisateur,
                titre='Rapport ajouté à votre projet',
                message=f'Un rapport a été ajouté à votre projet {instance.id_projet.titre or instance.id_projet.id_projet}.',
                type='rapport',
                id_cible=instance.id_rapport,
                role_cible=None
            )

@receiver(post_save, sender=Commentaire)
def create_notification_on_commentaire(sender, instance, created, **kwargs):
    if created:
        # Notifier le propriétaire du projet si différent du créateur
        if instance.id_utilisateur != instance.id_projet.id_utilisateur:
            Notification.objects.create(
                id_utilisateur=instance.id_projet.id_utilisateur,
                titre='Nouveau commentaire sur votre projet',
                message=f'Un nouveau commentaire a été ajouté à votre projet {instance.id_projet.titre or instance.id_projet.id_projet}.',
                type='commentaire',
                id_cible=instance.id_commentaire,
                role_cible=None
            )

@receiver(post_save, sender=Projet)
def check_overdue_projet(sender, instance, **kwargs):
    today = timezone.now().date()
    if instance.periode_fin and instance.periode_fin < today and instance.statut != 'Terminé':
        # Vérifier si une notification existe déjà pour éviter les doublons
        if not Notification.objects.filter(type='alerte', id_cible=instance.id_projet).exists():
            # Notifier le propriétaire du projet
            Notification.objects.create(
                id_utilisateur=instance.id_utilisateur,
                titre='Projet en retard',
                message=f'Le projet {instance.titre or instance.id_projet} a dépassé sa date de fin.',
                type='alerte',
                id_cible=instance.id_projet,
                role_cible=None
            )
            # Notifier les administrateurs
            admins = Utilisateur.objects.filter(role='admin')
            for admin in admins:
                Notification.objects.create(
                    id_utilisateur=admin,
                    titre='Projet en retard',
                    message=f'Le projet {instance.titre or instance.id_projet} ({instance.id_projet}) a dépassé sa date de fin.',
                    type='alerte',
                    id_cible=instance.id_projet,
                    role_cible='admin'
                )
