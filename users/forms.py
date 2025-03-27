from django import forms
from .models import Entite, Departement
from django.contrib.auth.models import User

class EntiteForm(forms.ModelForm):
    """Formulaire pour créer une entité."""
    class Meta:
        model = Entite
        fields = ['nom', 'code', 'description']

class AffecterDirecteurForm(forms.Form):
    """Formulaire pour affecter un directeur à une entité."""
    directeur = forms.ModelChoiceField(queryset=User.objects.filter(profil__role='enseignant'), label="Directeur")
    entite = forms.ModelChoiceField(queryset=Entite.objects.all(), label="Entité")

class DepartementForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = ['nom', 'code', 'entite', 'description','responsable']