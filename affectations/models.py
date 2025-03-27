from django.db import models
from django.contrib.auth.models import User
from cours.models import Cours  
from classes.models import Classe  

class Affectation(models.Model):
    """Modèle représentant l'affectation d'un enseignant à un cours et une classe"""
    enseignant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='affectations')
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='affectations')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='affectations')
    date_affectation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.enseignant.get_full_name()} - {self.cours.nom} - {self.classe.nom}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Vérifier que le cours est bien affecté à une classe définie dans l'entité
        if self.cours.formation.entite != self.classe.entite:
            raise ValidationError("Le cours doit être affecté à une classe définie dans la même entité")
    
    class Meta:
        verbose_name = "Affectation"
        verbose_name_plural = "Affectations"
        unique_together = ['enseignant', 'cours', 'classe']