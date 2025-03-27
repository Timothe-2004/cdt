from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from cours.models import Cours
from classes.models import Classe
from datetime import datetime, timedelta

class Seance(models.Model):
    """Modèle représentant une séance de cours dans le cahier de texte"""
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('valide', 'Validé'),
    ]
    
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='seances')
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='seances')
    enseignant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seances_enseignant')
    responsable_classe = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seances_responsable')
    date_seance = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    duree = models.DurationField(editable=False)
    description = models.TextField()
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='brouillon')
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.cours.nom} - {self.classe.nom} - {self.date_seance}"
    
    def save(self, *args, **kwargs):
        # Calculer la durée automatiquement
        self.duree = datetime.combine(self.date_seance, self.heure_fin) - datetime.combine(self.date_seance, self.heure_debut)
        super().save(*args, **kwargs)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        from django.db.models import Q
        
        # Vérifier que le cours est bien affecté à la classe
        if not self.cours.classes.filter(id=self.classe.id).exists():
            raise ValidationError("Le cours doit être affecté à la classe.")
        
        # Vérifier les conflits d'horaires pour la classe
        chevauchements_classe = Seance.objects.filter(
            classe=self.classe,
            date_seance=self.date_seance
        ).exclude(id=self.id).filter(
            Q(heure_debut__lt=self.heure_fin, heure_fin__gt=self.heure_debut)
        )
        
        if chevauchements_classe.exists():
            raise ValidationError("Cette classe a déjà une séance programmée sur ce créneau horaire.")
        
        # Vérifier les conflits d'horaires pour l'enseignant
        chevauchements_enseignant = Seance.objects.filter(
            enseignant=self.enseignant,
            date_seance=self.date_seance
        ).exclude(id=self.id).filter(
            Q(heure_debut__lt=self.heure_fin, heure_fin__gt=self.heure_debut)
        )
        
        if chevauchements_enseignant.exists():
            raise ValidationError("L'enseignant a déjà une séance programmée sur ce créneau horaire.")
    
    class Meta:
        verbose_name = "Séance"
        verbose_name_plural = "Séances"

class HistoriqueValidation(models.Model):
    """Modèle pour suivre l'historique des validations de séances"""
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, related_name='historique_validations')
    validee_par = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historique_validations')
    date_action = models.DateTimeField(auto_now_add=True)
    action = models.CharField(
        max_length=20, 
        choices=[('validation', 'Validation'), ('annulation', 'Annulation')]
    )
    
    class Meta:
        ordering = ['-date_action']
    
    def __str__(self):
        return f"{self.action} - {self.seance} - par {self.validee_par.get_full_name()}"