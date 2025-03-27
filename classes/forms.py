from django import forms
from .models import Classe

class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = ['nom', 'code', 'formations', 'annee_universitaire', 'effectif', 'entite_id']
        widgets = {
            'formations': forms.CheckboxSelectMultiple(),
        }