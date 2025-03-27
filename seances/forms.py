from django import forms
from .models import Seance
from classes.models import Classe  
from cours.models import Cours

class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ['classe', 'cours', 'enseignant', 'responsable_classe', 'date_seance', 'heure_debut', 'heure_fin', 'description', 'statut']
        widgets = {
            'date_seance': forms.DateInput(attrs={'type': 'date'}),
            'heure_debut': forms.TimeInput(attrs={'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if user:
            # Si l'utilisateur est un responsable de classe, limiter les choix
            try:
                classe_responsable = user.responsabilite_classe.classe
                self.fields['classe'].queryset = Classe.objects.filter(id=classe_responsable.id)
                self.fields['cours'].queryset = Cours.objects.filter(classes=classe_responsable)
            except:
                pass
    
    def clean(self):
        cleaned_data = super().clean()
        heure_debut = cleaned_data.get('heure_debut')
        heure_fin = cleaned_data.get('heure_fin')
        classe = cleaned_data.get('classe')
        cours = cleaned_data.get('cours')
        date = cleaned_data.get('date_seance')
        
        if heure_debut and heure_fin and heure_debut >= heure_fin:
            raise forms.ValidationError("L'heure de début doit être antérieure à l'heure de fin")
        
        if date and classe and heure_debut and heure_fin:
            from django.db.models import Q
            from .models import Seance
            
            # Vérifier chevauchements pour la classe
            chevauchements_classe = Seance.objects.filter(
                classe=classe, 
                date_seance=date  # Correction: utiliser date_seance au lieu de date
            ).exclude(id=self.instance.id if self.instance.pk else None).filter(
                Q(heure_debut__lt=heure_fin, heure_fin__gt=heure_debut)
            )
            
            if chevauchements_classe.exists():
                raise forms.ValidationError(
                    "Cette classe a déjà une séance programmée sur ce créneau horaire."
                )
            
            # Vérifier chevauchements pour l'enseignant
            if cours:
                chevauchements_enseignant = Seance.objects.filter(
                    cours__enseignant=cours.enseignant,
                    date_seance=date  # Correction: utiliser date_seance au lieu de date
                ).exclude(id=self.instance.id if self.instance.pk else None).filter(
                    Q(heure_debut__lt=heure_fin, heure_fin__gt=heure_debut)
                )
                
                if chevauchements_enseignant.exists():
                    raise forms.ValidationError(
                        "L'enseignant a déjà une séance programmée sur ce créneau horaire."
                    )
        
        return cleaned_data