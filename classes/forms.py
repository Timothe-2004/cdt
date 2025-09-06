from django import forms
from .models import Classe
from formations.models import Formation
from users.models import Departement

class ClasseForm(forms.ModelForm):
    departement = forms.ModelChoiceField(
        queryset=Departement.objects.all(),
        required=False,
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'}),
        label="Département"
    )

    formation = forms.ModelChoiceField(
        queryset=Formation.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'formation-select'}),
        label="Formation"
    )

    est_tronc_commun = forms.ChoiceField(
        choices=[(1, 'Oui'), (0, 'Non')],
        widget=forms.RadioSelect,
        label="Est-ce une classe de tronc commun ?",
        required=True
    )

    class Meta:
        model = Classe
        fields = ['departement', 'formation', 'nom', 'code', 'annee_universitaire', 'effectif', 'est_tronc_commun']
        widgets = {
            'annee_universitaire': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Exemple : 2024-2025'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        departement_id = kwargs.pop('departement_id', None)
        super().__init__(*args, **kwargs)

        if user and hasattr(user, 'profil') and user.profil.entite:
            self.fields['departement'].queryset = Departement.objects.filter(entite=user.profil.entite)

        if departement_id:
            self.fields['formation'].queryset = Formation.objects.filter(departement_id=departement_id)
        else:
            self.fields['formation'].queryset = Formation.objects.none()

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})