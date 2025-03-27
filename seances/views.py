# views.py (seances)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Seance
from classes.models import Classe
from .forms import SeanceForm
from cours.models import Cours
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Seance, HistoriqueValidation
from .serializers import SeanceSerializer, HistoriqueValidationSerializer
from .permissions import EstResponsableClasse, PeutValiderSeance
from django.contrib.auth.decorators import user_passes_test

@login_required
def liste_seances(request):
    print(f"Utilisateur connecté : {request.user.username}, Rôle : {request.user.profil.role}")
    if request.user.profil.role == 'enseignant':
        seances = Seance.objects.filter(cours__enseignant=request.user)
    else:
        seances = Seance.objects.all()
    print(f"Séances récupérées : {seances}")
    return render(request, 'seances/liste_seances.html', {'seances': seances})

@login_required
def planifier_seance(request, cours_id=None):
    cours = None
    if cours_id:
        cours = get_object_or_404(Cours, id=cours_id)
        # Vérifier que l'utilisateur est l'enseignant du cours
        if request.user != cours.enseignant and not request.user.is_superuser:
            messages.error(request, "Vous n'êtes pas autorisé à planifier des séances pour ce cours.")
            return redirect('liste_cours')
    
    if request.method == 'POST':
        form = SeanceForm(request.POST, user=request.user)
        if form.is_valid():
            seance = form.save(commit=False)
            # Calculer la durée automatiquement
            from datetime import datetime
            debut = datetime.combine(seance.date, seance.heure_debut)
            fin = datetime.combine(seance.date, seance.heure_fin)
            duree = (fin - debut).seconds // 3600
            seance.duree = duree
            seance.save()
            
            messages.success(request, 'Séance planifiée avec succès!')
            return redirect('detail_cours', cours_id=seance.cours.id)
    else:
        initial = {}
        if cours:
            initial['cours'] = cours
        form = SeanceForm(user=request.user, initial=initial)
    
    return render(request, 'seances/planifier_seance.html', {
        'form': form,
        'cours': cours
    })

@login_required
@user_passes_test(lambda u: u.profil.role == 'responsable_classe')
def ajouter_seance(request):
    if request.method == 'POST':
        form = SeanceForm(request.POST, user=request.user)
        if form.is_valid():
            seance = form.save(commit=False)
            seance.responsable_classe = request.user
            seance.save()
            messages.success(request, 'Séance ajoutée avec succès!')
            return redirect('seances:liste_seances')
    else:
        form = SeanceForm(user=request.user)
    return render(request, 'seances/ajouter_seance.html', {'form': form})

@login_required
def detail_seance(request, seance_id):
    seance = get_object_or_404(Seance, id=seance_id)
    return render(request, 'seances/detail_seance.html', {'seance': seance})

@login_required
def modifier_seance(request, seance_id):
    seance = get_object_or_404(Seance, id=seance_id)
    if request.method == 'POST':
        form = SeanceForm(request.POST, instance=seance)
        if form.is_valid():
            form.save()
            return redirect('seances:liste_seances')
    else:
        form = SeanceForm(instance=seance)
    return render(request, 'seances/ajouter_seance.html', {'form': form})

class SeanceViewSet(viewsets.ModelViewSet):
    queryset = Seance.objects.all()
    serializer_class = SeanceSerializer
    permission_classes = [IsAuthenticated, EstResponsableClasse]

    @action(detail=True, methods=['post'], permission_classes=[PeutValiderSeance])
    def valider(self, request, pk=None):
        seance = self.get_object()
        seance.statut = 'valide'
        seance.save()
        
        # Enregistrer l'historique de validation
        HistoriqueValidation.objects.create(
            seance=seance,
            validee_par=request.user,
            action='validation'
        )
        
        return Response({'status': 'Séance validée'})

class HistoriqueValidationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistoriqueValidation.objects.all()
    serializer_class = HistoriqueValidationSerializer
    permission_classes = [IsAuthenticated]

class DashboardResponsableClasseViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def seances_creees(self, request):
        user = request.user
        seances = Seance.objects.filter(responsable_classe=user)
        serializer = SeanceSerializer(seances, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def seances_en_attente(self, request):
        user = request.user
        seances = Seance.objects.filter(responsable_classe=user, statut='brouillon')
        serializer = SeanceSerializer(seances, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def historique(self, request):
        user = request.user
        historique = HistoriqueValidation.objects.filter(seance__responsable_classe=user)
        serializer = HistoriqueValidationSerializer(historique, many=True)
        return Response(serializer.data)