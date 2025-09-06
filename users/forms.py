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
        fields = ['nom', 'code', 'description', 'responsable']  # Removed 'entite' from visible fields

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Retrieve the logged-in user
        super().__init__(*args, **kwargs)

        if user and hasattr(user, 'profil') and user.profil.entite:
            # Automatically set the 'entite' field based on the user's entity
            self.instance.entite = user.profil.entite

        # Display full names for the 'responsable' field and include both 'chef_département' and 'enseignant' roles
        self.fields['responsable'].queryset = User.objects.filter(profil__role__in=['chef_département', 'enseignant'])
        self.fields['responsable'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

        # Add CSS classes for better styling
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})