from django.db import models
from django.utils import timezone
from axes.models import Axe


def generate_objectif_custom_id():
    last_objectif = Objectif.objects.all().order_by('id_objectif').last()
    if not last_objectif:
        return 'OBJ001'
    objectif_id = last_objectif.id_objectif
    objectif_int = int(objectif_id.split('OBJ')[-1])
    new_objectif_int = objectif_int + 1
    new_objectif_id = f'OBJ{new_objectif_int:03d}'
    return new_objectif_id

class Objectif(models.Model):
    id_objectif = models.CharField(primary_key=True, max_length=10, default=generate_objectif_custom_id, editable=False)
    id_axe = models.ForeignKey(Axe, on_delete=models.CASCADE, db_column='id_axe')
    intitule = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.intitule or f"Objectif {self.id_objectif}"
    class Meta:
        db_table = 'objectif'

    