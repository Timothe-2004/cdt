# users/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Entite(models.Model):
    """Modèle représentant une UFR, faculté ou école"""
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Entité"
        verbose_name_plural = "Entités"

class Departement(models.Model):
    """Modèle représentant un département académique."""
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    entite = models.ForeignKey(Entite, on_delete=models.CASCADE, related_name='departements')
    description = models.TextField(blank=True, null=True)
    
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='departement_responsable')
    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"

class ProfilUtilisateur(models.Model):
    """Modèle représentant le profil d'un utilisateur"""
    ROLES_CHOICES = [
        ('admin', 'Administrateur'),
        ('enseignant', 'Enseignant'),
        ('responsable_classe', 'Responsable de Classe'),
        ('directeur_academique', 'Directeur Academique'),
        ('controleur', 'Controleur'),
        ('chef_département', 'Chef de Département')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    role = models.CharField(max_length=50, choices=ROLES_CHOICES)
    
    # Relation directe avec Entite
    entite = models.ForeignKey(Entite, on_delete=models.SET_NULL, null=True, blank=True, related_name='profils')
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True, blank=True, related_name='profils')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profil Utilisateur"
        verbose_name_plural = "Profils Utilisateurs"