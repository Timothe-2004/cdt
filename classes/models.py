# classes/models.py
from django.db import models
from django.contrib.auth.models import User

class Classe(models.Model):
    """Modèle représentant une classe académique"""
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    
    # Utiliser des chaînes pour éviter les imports directs
    formations = models.ManyToManyField('formations.Formation', related_name='classes_associees', blank=True)
    
    annee_universitaire = models.CharField(max_length=9)  # Exemple : "2024-2025"
    effectif = models.PositiveIntegerField()  # Nombre d'étudiants dans la classe
    
    # Utiliser un identifiant au lieu d'une relation directe
    entite_id = models.ForeignKey('users.Entite', on_delete=models.CASCADE, related_name='classes')
    date_creation = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='classes_responsables')
    est_tronc_commun = models.BooleanField(default=False, verbose_name="Est-ce une classe de tronc commun ?")

    def get_entite(self):
        from users.models import Entite  # Import local
        return Entite.objects.get(pk=self.entite_id)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Classe"
        verbose_name_plural = "Classes"

class ResponsableClasse(models.Model):
    # Utiliser des chaînes et des identifiants
    user_id = models.PositiveIntegerField()
    classe_id = models.PositiveIntegerField()

    def get_user(self):
        from django.contrib.auth.models import User
        return User.objects.get(pk=self.user_id)

    def get_classe(self):
        return Classe.objects.get(pk=self.classe_id)

    def __str__(self):
        user = self.get_user()
        classe = self.get_classe()
        return f"{user.get_full_name()} - {classe}"

    def clean(self):
        from users.models import ProfilUtilisateur
        from django.core.exceptions import ValidationError

        try:
            user = self.get_user()
            profil = ProfilUtilisateur.objects.get(user=user)
            if profil.role != 'responsable_classe':
                raise ValidationError("L'utilisateur doit avoir le rôle de responsable de classe")
        except ProfilUtilisateur.DoesNotExist:
            raise ValidationError("L'utilisateur doit avoir un profil")