from django.db import models

from projets.models import Projet
from utilisateurs.models import Utilisateur

def custom_id():
    last_rapport = Rapport.objects.all().order_by('id_rapport').last()
    if not last_rapport:
        return 'R0001'
    rapport_id = last_rapport.id_rapport
    rapport_int = int(rapport_id.split('R')[-1])
    new_rapport_int = rapport_int + 1
    new_rapport_id = 'R' + str(new_rapport_int).zfill(4)
    return new_rapport_id

class Rapport(models.Model):
    PERIODE = [
        ('Hebdomadaire', 'Hebdomadaire'),
        ('Mensuelle', 'Mensuelle'),
        ('Trimestrielle', 'Trimestrielle'),
        ('Semestrielle', 'Semestrielle'),
        ('Annuelle', 'Annuelle'),
    ]
    id_rapport = models.CharField(primary_key=True, max_length=10, default=custom_id, editable=False)
    id_projet = models.ForeignKey(Projet, on_delete=models.CASCADE, db_column='id_projet')
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE , db_column='id_utilisateur')
    periodicite = models.CharField(max_length=50, null=True, blank=True, choices=PERIODE)
    statut = models.CharField(max_length=255, null=True, blank=True)
    observation = models.CharField(max_length=255, null=True, blank=True)
    solution = models.CharField(max_length=255, null=True, blank=True)
    probleme = models.CharField(max_length=255, null=True, blank=True)
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Rapport {self.id_rapport} - {self.id_projet}"

    class Meta:
        db_table = 'rapport'
