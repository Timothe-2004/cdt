from django import forms
from .models import Cours
from classes.models import Classe
from formations.models import Formation
from users.models import User, Departement

class CoursForm(forms.ModelForm):
    enseignant = forms.ModelChoiceField(
        queryset=User.objects.filter(profil__role__in=['enseignant', 'directeur_academique', 'chef_departement']),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Enseignant"
    )

    class Meta:
        model = Cours
        fields = ['nom', 'code', 'volume_horaire_total', 'volume_theorie', 'volume_tp', 'volume_td', 'enseignant']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du cours'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code du cours'}),
            'volume_horaire_total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Volume horaire total'}),
            'volume_theorie': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Volume théorie'}),
            'volume_tp': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Volume TP'}),
            'volume_td': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Volume TD'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and hasattr(user, 'profil'):
            if user.profil.role == 'directeur_academique':
                self.instance.entite = user.profil.entite
            elif user.profil.role == 'chef_département' and user.profil.departement:
                self.instance.entite = user.profil.departement.entite

        self.fields.pop('entite', None)  # Remove the 'entite' field from the form
        self.fields['enseignant'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

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