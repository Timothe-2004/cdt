from django import forms
from .models import Cours
from classes.models import Classe
from formations.models import Formation
from users.models import Entite, Departement

class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['nom', 'code'
        '', 'volume_horaire_total', 'volume_theorie', 'volume_tp', 'volume_td',
                  'formations', 'classes', 'enseignant']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom du cours'}),
            'code': forms.TextInput(attrs={'placeholder': 'Code du cours'}),
            'volume_horaire_total': forms.NumberInput(attrs={'min': 0}),
            'volume_theorie': forms.NumberInput(attrs={'min': 0}),
            'volume_tp': forms.NumberInput(attrs={'min': 0}),
            'volume_td': forms.NumberInput(attrs={'min': 0}),
            'formations': forms.SelectMultiple(attrs={'class': 'select2'}),
            'classes': forms.SelectMultiple(attrs={'class': 'select2'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        volume_horaire_total = cleaned_data.get('volume_horaire_total')
        volume_theorie = cleaned_data.get('volume_theorie')
        volume_tp = cleaned_data.get('volume_tp')
        volume_td = cleaned_data.get('volume_td')

        if volume_horaire_total and (volume_theorie + volume_tp + volume_td != volume_horaire_total):
            raise forms.ValidationError("La somme des volumes (théorie, TP, TD) doit être égale au volume horaire total.")

        return cleaned_data


class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['nom', 'code', 'objectifs', 'credits', 'departement']
        widgets = {
            'objectifs': forms.Textarea(attrs={'rows': 3}),
        }


class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = ['nom', 'code', 'formations', 'annee_universitaire', 'effectif', 'entite_id']
        widgets = {
            'formations': forms.CheckboxSelectMultiple(),
        }