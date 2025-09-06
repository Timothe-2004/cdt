from django import forms
from .models import Formation
from users.models import Departement

class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['nom', 'code', 'objectifs', 'credits', 'departement']  
        widgets = {
            'objectifs': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Retrieve the logged-in user
        super().__init__(*args, **kwargs)

        if user and hasattr(user, 'profil') and user.profil.entite:
            # Filter departments by the entity of the Director Académique
            self.fields['departement'].queryset = Departement.objects.filter(entite=user.profil.entite)

        # Add CSS classes for better styling
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})