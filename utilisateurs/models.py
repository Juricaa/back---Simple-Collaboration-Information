# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

from regions.models import Region

def custom_id():
    try:
        last_user = Utilisateur.objects.all().order_by('id_utilisateur').last()
        if not last_user:
            return 'U001'
        user_id = last_user.id_utilisateur
        user_int = int(user_id.split('U')[-1])
        new_user_int = user_int + 1
        new_user_id = f'U{new_user_int:03d}'
        return new_user_id
    except:
        # Retourne une valeur par défaut pendant les migrations
        return 'U001'

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('Role', 'admin')
        extra_fields.setdefault('Actif', True)
        return self.create_user(email, password, **extra_fields)

class Utilisateur(AbstractBaseUser):
    id_utilisateur = models.CharField(primary_key=True, max_length=10, default=custom_id, editable=False)
    id_region = models.ForeignKey(Region, on_delete=models.CASCADE, db_column='id_region', null=True, blank=True)
    nom = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, max_length=255)
    role = models.CharField(max_length=255, null=True, blank=True)
    mot_de_passe = models.CharField(max_length=255, null=True, blank=True)  # À utiliser avec set_password()
    actif = models.BooleanField(default=True)
    date_creation = models.DateField(auto_now_add=True)

    objects = UtilisateurManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'id_region']

    def __str__(self):
        return self.nom or self.email

    class Meta:
        db_table = 'utilisateur'