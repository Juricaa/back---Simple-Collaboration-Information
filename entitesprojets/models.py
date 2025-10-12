from django.db import models

from entites.models import Entite
from projets.models import Projet

class EntiteProjet(models.Model):
    id_entite = models.ForeignKey(Entite, on_delete=models.CASCADE, db_column='id_entite')
    id_projet = models.ForeignKey(Projet, on_delete=models.CASCADE, db_column='id_projet')

    class Meta:
        unique_together = ('id_entite', 'id_projet')

    def __str__(self):
        return f"{self.id_entite} - {self.id_projet}"
    class Meta:
        db_table = 'entite_projet'
