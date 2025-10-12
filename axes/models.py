from django.db import models

from utilisateurs.models import Utilisateur

def generate_axe_custom_id():
    last_axe = Axe.objects.all().order_by('id_axe').last()
    if not last_axe:
        return 'AXE001'
    axe_id = last_axe.id_axe
    axe_int = int(axe_id.split('AXE')[-1])
    new_axe_int = axe_int + 1
    new_axe_id = f'AXE{new_axe_int:03d}'
    return new_axe_id

class Axe(models.Model):
    id_axe = models.CharField(primary_key=True, max_length=10, default=generate_axe_custom_id, editable=False)
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    annee = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=255, null=True, blank=True)
    

    def __str__(self):
        return self.titre or f"Axe {self.id_axe}"

    class Meta:
        db_table = 'axe'
