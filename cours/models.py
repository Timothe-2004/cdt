# cours/models.py
from django.db import models
from django.contrib.auth.models import User
from formations.models import Formation

class Cours(models.Model):
    """Modèle représentant un cours avec volume horaire et répartition"""
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    volume_horaire_total = models.IntegerField()
    volume_theorie = models.IntegerField()
    volume_tp = models.IntegerField()
    volume_td = models.IntegerField()
    
    # Un cours peut être dans plusieurs formations (ManyToMany)
    formations = models.ManyToManyField(Formation, related_name='cours_associes', blank=True)
    
    # Un cours peut être suivi par plusieurs classes (ManyToMany)
    classes = models.ManyToManyField('classes.Classe', related_name='cours', blank=True)
    
    # L'enseignant reste inchangé
    enseignant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cours')
    entite = models.ForeignKey('users.Entite', on_delete=models.CASCADE, null=True, blank=True, related_name='cours')
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"

