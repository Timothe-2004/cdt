# forms.py
from django import forms
from .models import Seance
from classes.models import Classe  
from cours.models import Cours

class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ['cours', 'date_seance', 'heure_debut', 'heure_fin', 'description']
        widgets = {
            'date_seance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'heure_debut': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'cours': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Récupération de la classe du responsable
        if user and hasattr(user, 'profil') and user.profil.role == 'responsable_classe':
            classe = Classe.objects.filter(responsable=user).first()
            if classe:
                # Stocker la classe sur l'instance du form pour l'utiliser dans la vue
                self.classe_responsable = classe
                # Filtrer les cours liés à cette classe
                self.fields['cours'].queryset = Cours.objects.filter(classes=classe)
            else:
                self.fields['cours'].queryset = Cours.objects.none()
        else:
            self.fields['cours'].queryset = Cours.objects.none()
