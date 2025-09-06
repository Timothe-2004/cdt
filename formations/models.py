from django.db import models
from django.contrib.auth.models import User
from users.models import Departement


class Formation(models.Model):

    nom  = models.CharField(max_length=100)

    code = models.CharField(max_length=20, unique=True)

    objectifs = models.TextField(blank=True, null=True)

    credits = models.IntegerField()

    departement = models.ForeignKey(
        Departement,
        on_delete=models.SET_NULL,
        null=True,  
        related_name='formations'
    )

    responsable = models.ForeignKey( User, on_delete=models.SET_NULL, null=True, related_name='formations_responsable')
      
      
      
    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"
