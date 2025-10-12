from django.db import models

def generate_region_custom_id():
    last_region = Region.objects.all().order_by('id_region').last()
    if not last_region:
        return 'REG001'
    region_id = last_region.id_region
    region_int = int(region_id.split('REG')[-1])
    new_region_int = region_int + 1
    new_region_id = f'REG{new_region_int:03d}'
    return new_region_id

class Region(models.Model):
    id_region = models.CharField(primary_key=True, max_length=10, default=generate_region_custom_id, editable=False)
    nom = models.CharField(max_length=255, null=True, blank=True)
    code_postale = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.Nom or f"Region {self.Id_region}"

    class Meta:
        db_table = 'region'
