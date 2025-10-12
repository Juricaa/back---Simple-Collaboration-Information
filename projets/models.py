from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.validators import MinValueValidator
from objectifs.models import Objectif
from utilisateurs.models import Utilisateur  

def cusstomId():
    last_projet = Projet.objects.all().order_by('id_projet').last()
    if not last_projet:
        return 'PRJ0001'
    projet_id = last_projet.id_projet
    projet_int = int(projet_id.split('PRJ')[-1])
    new_projet_int = projet_int + 1
    new_projet_id = 'PRJ' + str(new_projet_int).zfill(4)
    return new_projet_id


class Projet(models.Model):
    id_projet = models.CharField(primary_key=True, max_length=10, default=cusstomId, editable=False)
    id_objectif = models.ForeignKey(Objectif, on_delete=models.CASCADE, db_column='id_objectif')
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, db_column='id_utilisateur')
    titre = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    statut = models.CharField(max_length=255, null=True, blank=True)
    indicateur = models.CharField(max_length=255, null=True, blank=True)
    unite_indicateur = models.CharField(max_length=255, null=True, blank=True)
    valeur_cible = models.CharField(max_length=255, null=True, blank=True)
    baseline = models.CharField(max_length=255, null=True, blank=True)
    budget_estimatif = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    impact_socio_eco = models.CharField(max_length=255, null=True, blank=True)
    periode_debut = models.DateField(null=True, blank=True)
    periode_fin = models.DateField(null=True, blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_validation = models.DateTimeField(null=True,blank=True)
    commentaire_evaluation= models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.titre or f"Projet {self.id_projet}"
    class Meta:
        db_table = 'projet'

    