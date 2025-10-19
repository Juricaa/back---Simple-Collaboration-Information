from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from notifications.models import Notification
from rapports.models import Rapport
from commentaires.models import Commentaire
from projets.models import Projet
from utilisateurs.models import Utilisateur

def check_overdue_reports(projet):
    """Vérifier les rapports hebdomadaires en retard pour un projet."""
    today = timezone.now().date()
    # Supposons que les rapports hebdomadaires doivent être soumis chaque semaine
    # Trouver la dernière date de rapport soumis
    last_rapport = Rapport.objects.filter(id_projet=projet).order_by('-date_creation').first()
    if last_rapport:
        last_date = last_rapport.date_creation.date()
        # Si plus d'une semaine depuis le dernier rapport et que le projet n'est pas terminé
        if (today - last_date) > timedelta(days=7) and projet.statut != 'Terminé':
            # Vérifier si une notification existe déjà
            if not Notification.objects.filter(type='alerte', id_cible=projet.id_projet, titre__icontains='rapport hebdomadaire').exists():
                # Notifier le propriétaire du projet
                Notification.objects.create(
                    id_utilisateur=projet.id_utilisateur,
                    titre='Rapport hebdomadaire en retard',
                    message=f'Le rapport hebdomadaire pour le projet {projet.titre or projet.id_projet} est en retard.',
                    type='alerte',
                    id_cible=projet.id_projet,
                    role_cible=None
                )
                # Notifier les administrateurs
                admins = Utilisateur.objects.filter(role='admin')
                for admin in admins:
                    Notification.objects.create(
                        id_utilisateur=admin,
                        titre='Rapport hebdomadaire en retard',
                        message=f'Le rapport hebdomadaire pour le projet {projet.titre or projet.id_projet} ({projet.id_projet}) est en retard.',
                        type='alerte',
                        id_cible=projet.id_projet,
                        role_cible='admin'
                    )

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

    # Vérifier les rapports en retard pour le projet
    check_overdue_reports(instance.id_projet)

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
        # Notifier l'auteur du commentaire parent si c'est une réponse
        if instance.id_commentaire_parent and instance.id_commentaire_parent.id_utilisateur != instance.id_utilisateur:
            Notification.objects.create(
                id_utilisateur=instance.id_commentaire_parent.id_utilisateur,
                titre='Réponse à votre commentaire',
                message=f'Quelqu\'un a répondu à votre commentaire sur le projet {instance.id_projet.titre or instance.id_projet.id_projet}.',
                type='commentaire',
                id_cible=instance.id_commentaire,
                role_cible=None
            )
        # Alerter les administrateurs
        admins = Utilisateur.objects.filter(role='admin')
        for admin in admins:
            Notification.objects.create(
                id_utilisateur=admin,
                titre='Nouveau commentaire ajouté',
                message=f'Un nouveau commentaire a été ajouté au projet {instance.id_projet.titre or instance.id_projet.id_projet}.',
                type='commentaire',
                id_cible=instance.id_commentaire,
                role_cible='admin'
            )

@receiver(post_save, sender=Projet)
def handle_projet_notifications(sender, instance, created, **kwargs):
    if created:
        # Notifier les administrateurs d'un nouveau projet
        admins = Utilisateur.objects.filter(role='admin')
        for admin in admins:
            Notification.objects.create(
                id_utilisateur=admin,
                titre='Nouveau projet ajouté',
                message=f'Un nouveau projet {instance.titre or instance.id_projet} a été ajouté.',
                type='projet',
                id_cible=instance.id_projet,
                role_cible='admin'
            )

    # Vérifier si le projet est en retard (à chaque sauvegarde)
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
