from django.db import models

from rapports.models import Rapport

def custom_realisation_id():
    last_realisation = Realisation.objects.all().order_by('id_realisation').last()
    if not last_realisation:
        return 'R0001'
    realisation_id = last_realisation.id_realisation
    realisation_int = int(realisation_id.split('R')[-1])
    new_realisation_int = realisation_int + 1
    new_realisation_id = 'R' + str(new_realisation_int).zfill(4)
    return new_realisation_id

class Realisation(models.Model):
    id_realisation = models.CharField(primary_key=True, max_length=10, default=custom_realisation_id, editable=False)
    id_rapport = models.ForeignKey(Rapport, on_delete=models.CASCADE, db_column='id_rapport')
    contenue = models.CharField(max_length=255, null=True, blank=True)
    valeur_realise = models.IntegerField(default=0)
    debut_realisation = models.DateField(null=True, blank=True)
    fin_realisation = models.DateField(null=True, blank=True)
    ecart_realisation = models.CharField(max_length=255, null=True, blank=True)
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Réalisation {self.id_realisation}"

    class Meta:
        db_table = 'realisation'
