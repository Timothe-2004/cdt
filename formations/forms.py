from django import forms
from .models import Formation
from users.models import Departement

class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['nom', 'code', 'objectifs', 'credits', 'departement']  # Suppression de `responsable`
        widgets = {
            'objectifs': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['departement'].queryset = Departement.objects.all()