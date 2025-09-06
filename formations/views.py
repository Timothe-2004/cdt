# views.py (formations)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Formation, Departement  
from .forms import FormationForm  
from classes.models import Classe  
from cours.models import Cours    
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import JsonResponse
from django.db.models import Q

from .serializers import FormationSerializer
from .permissions import EstDirecteurAcademique
from users.permissions import EstDirecteurAcademique
from users.views import is_directeur_academique


def is_admin_or_chef(user):
    return user.is_superuser or hasattr(user, 'departement_dirige')

@login_required
@user_passes_test(is_directeur_academique)
def liste_formations(request):
    query = request.GET.get('q', '')
    formations = Formation.objects.filter(departement__entite=request.user.profil.entite)

    if query:
        formations = formations.filter(
            Q(nom__icontains=query) | Q(code__icontains=query)
        )

    return render(request, 'formations/liste_formations.html', {'formations': formations, 'query': query})

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
        form = FormationForm(request.POST, user=request.user)  # Pass the logged-in user to the form
        if form.is_valid():
            formation = form.save(commit=False)
            # Vérifiez que le département existe avant de l'assigner
            departement = form.cleaned_data.get('departement')
            if departement and Departement.objects.filter(id=departement.id).exists():
                formation.departement = departement
            else:
                messages.error(request, "Le département sélectionné n'existe pas ou est invalide.")
                return render(request, 'formations/ajouter_formation.html', {'form': form})
            formation.save()
            messages.success(request, 'Formation créée avec succès!')
            return redirect('formations:liste_formations')
    else:
        form = FormationForm(user=request.user)  # Pass the logged-in user to the form
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

@login_required
def supprimer_formation(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)
    if request.method == 'POST':
        formation.delete()
        messages.success(request, 'Formation supprimée avec succès!')
        return redirect('formations:liste_formations')
    return render(request, 'formations/confirm_supprimer_formation.html', {'formation': formation})

@login_required
def get_formations_by_departement(request):
    departement_id = request.GET.get('departement_id')
    if not departement_id:
        return JsonResponse({'error': 'No department ID provided'}, status=400)

    formations = Formation.objects.filter(departement_id=departement_id).values('id', 'nom')
    return JsonResponse(list(formations), safe=False)

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
