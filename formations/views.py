# views.py (formations)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Formation, Departement  # Importez uniquement les modèles existants
from .forms import FormationForm  # Ajout de l'importation manquante pour le formulaire FormationForm

from classes.models import Classe  # Importez Classe depuis l'application classes
from cours.models import Cours    # Importez Cours depuis l'application cours
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# Supprimez cette ligne problématique :
# from .models import Formation, Classe, Cours
from .serializers import FormationSerializer
from .permissions import EstDirecteurAcademique
from users.permissions import EstDirecteurAcademique


def is_admin_or_chef(user):
    return user.is_superuser or hasattr(user, 'departement_dirige')

@login_required
def liste_formations(request):
    formations = Formation.objects.all()
    return render(request, 'formations/liste_formations.html', {'formations': formations})

@login_required
def detail_formation(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)
    
    return render(request, 'formations/detail_formation.html', {
        'formation': formation
        
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Formation, Departement
from .forms import FormationForm

def is_admin_or_chef(user):
    return user.is_superuser or hasattr(user, 'departement_dirige')

@login_required
def ajouter_formation(request):
    if request.method == 'POST':
        form = FormationForm(request.POST)
        if form.is_valid():
            formation = form.save(commit=False)
            # Vérifiez que le département existe avant de l'assigner
            departement = form.cleaned_data.get('departement')
            if departement and Departement.objects.filter(id=departement.id).exists():
                formation.departement = departement
            else:
                messages.error(request, "Le département sélectionné n'existe pas ou est invalide.")
                return render(request, 'formations/ajouter_formation.html', {'form': form})
            # Suppression de l'attribution de responsable si elle n'est plus nécessaire
            # formation.responsable = request.user
            formation.save()
            messages.success(request, 'Formation créée avec succès!')
            return redirect('formations:liste_formations')
    else:
        form = FormationForm()
    return render(request, 'formations/ajouter_formation.html', {'form': form})

@login_required
def modifier_formation(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)
    if request.method == 'POST':
        form = FormationForm(request.POST, instance=formation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formation modifiée avec succès!')
            return redirect('formations:liste_formations')
    else:
        form = FormationForm(instance=formation)
    return render(request, 'formations/modifier_formation.html', {'form': form, 'formation': formation})

class FormationViewSet(viewsets.ModelViewSet):
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer
    permission_classes = [IsAuthenticated, EstDirecteurAcademique]

    def get_queryset(self):
        user = self.request.user
        if user.profil.role == 'directeur_academique':
            return Formation.objects.filter(departement__entite=user.profil.entite)
        return super().get_queryset()

class ClasseViewSet(viewsets.ModelViewSet):
    queryset = Classe.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.profil.role == 'directeur_academique':
            return Classe.objects.filter(formation__departement__entite=user.profil.entite)
        return super().get_queryset()

class CoursViewSet(viewsets.ModelViewSet):
   
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.profil.role == 'directeur_academique':
            return Cours.filter(formation__departement__entite=user.profil.entite)
        return super().get_queryset()
