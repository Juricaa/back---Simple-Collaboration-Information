from django.db import models

def custom_entite_id():
    last_entite = Entite.objects.all().order_by('id_entite').last()
    if not last_entite:
        return 'E0001'
    entite_id = last_entite.id_entite
    entite_int = int(entite_id.split('E')[-1])
    new_entite_int = entite_int + 1
    new_entite_id = 'E' + str(new_entite_int).zfill(4)
    return new_entite_id

class Entite(models.Model):
    id_entite = models.CharField(primary_key=True, max_length=10, default=custom_entite_id, editable=False)
    nom = models.CharField(max_length=255, null=True, blank=True)
    abreviation = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nom or f"Entité {self.id_entite}"

    class Meta:
        db_table = 'entite'
