from django.db import models


# Create your models here.
class Finch(models.Model):
    species = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    habitat = models.CharField(max_length=300)
    note = models.CharField(max_length=750)

    def __str__(self):
        return self.species
