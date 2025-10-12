from django.utils import timezone
from django.db import models

from projets.models import Projet
from utilisateurs.models import Utilisateur

def custom_commentaire_id():
    last_commentaire = Commentaire.objects.all().order_by('id_commentaire').last()
    if not last_commentaire:
        return 'C0001'
    commentaire_id = last_commentaire.id_commentaire
    commentaire_int = int(commentaire_id.split('C')[-1])
    new_commentaire_int = commentaire_int + 1
    new_commentaire_id = 'C' + str(new_commentaire_int).zfill(4)
    return new_commentaire_id

class Commentaire(models.Model):
    id_commentaire = models.CharField(primary_key=True, max_length=10, default=custom_commentaire_id, editable=False)
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, db_column='id_utilisateur')
    id_commentaire_parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, db_column='id_commentaire_parent')
    id_projet = models.ForeignKey(Projet, on_delete=models.CASCADE, db_column='id_projet')
    contenue = models.CharField(max_length=255, null=True, blank=True)
    date_creation = models.DateField(auto_now_add=True)
    etat = models.CharField(max_length=255, null=True, blank=True)
    nb_jaime = models.IntegerField(default=0)

    def __str__(self):
        return f"Commentaire {self.id_commentaire}"
    
    class Meta:
        db_table = 'commentaire'

    