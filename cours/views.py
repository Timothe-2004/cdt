from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cours
from classes.models import Classe
from formations.models import Formation
from .forms import CoursForm
from seances.models import Seance
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CoursSerializer, ClasseSerializer, SeanceSerializer
from users.permissions import EstEnseignant, EstDirecteurAcademique, EstChefDepartement, EstAdministrateur

@login_required
def liste_cours(request):
    cours = Cours.objects.filter(enseignant=request.user)
    return render(request, 'cours/liste_cours.html', {'cours': cours})

@login_required
def detail_cours(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    seances = cours.seances.all().order_by('date_seance')  # Corrected field name
    formations = cours.formations.all()
    classes = cours.classes.all()

    if request.user != cours.enseignant and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas accès à ce cours.")
        return redirect('liste_cours')

    return render(request, 'cours/detail_cours.html', {
        'cours': cours,
        'seances': seances,
        'formations': formations,
        'classes': classes
    })

@login_required
def cahier_texte(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    seances = cours.seances.all().order_by('date')

    if request.user != cours.enseignant and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas accès à ce cahier de texte.")
        return redirect('liste_cours')

    return render(request, 'cours/cahier_texte.html', {
        'cours': cours,
        'seances': seances
    })

@login_required
def ajouter_cours(request):
    if request.method == 'POST':
        form = CoursForm(request.POST)
        if form.is_valid():
            cours = form.save(commit=False)
            cours.enseignant = request.user
            cours.save()
            # Sauvegarde des relations ManyToMany
            form.save_m2m()
            messages.success(request, 'Cours créé avec succès!')
            return redirect('cours:detail_cours', cours_id=cours.id)  # Corrected namespace
    else:
        form = CoursForm()

    return render(request, 'cours/ajouter_cours.html', {'form': form})

@login_required
def modifier_cours(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    
    if request.user != cours.enseignant and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas l'autorisation de modifier ce cours.")
        return redirect('liste_cours')
    
    if request.method == 'POST':
        form = CoursForm(request.POST, instance=cours)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cours modifié avec succès!')
            return redirect('detail_cours', cours_id=cours.id)
    else:
        form = CoursForm(instance=cours)
    
    return render(request, 'cours/modifier_cours.html', {'form': form, 'cours': cours})

@login_required
def supprimer_cours(request, cours_id):
    try:
        cours = Cours.objects.get(id=cours_id)
    except Cours.DoesNotExist:
        messages.error(request, "Le cours demandé n'existe pas.")
        return redirect('cours:liste_cours')

    if request.method == 'POST':
        cours.delete()
        messages.success(request, 'Cours supprimé avec succès!')
        return redirect('cours:liste_cours')

    return render(request, 'cours/supprimer_cours.html', {'cours': cours})

class DashboardEnseignantViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def cours_affectes(self, request):
        user = request.user
        cours = Cours.objects.filter(enseignant=user)
        serializer = CoursSerializer(cours, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def seances_realisees(self, request):
        user = request.user
        seances = Seance.objects.filter(cours__enseignant=user, statut='valide')
        serializer = SeanceSerializer(seances, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def heures_effectuees(self, request):
        user = request.user
        cours = Cours.objects.filter(enseignant=user)
        data = []
        for cour in cours:
            seances = Seance.objects.filter(cours=cour, statut='valide')
            heures_effectuees = sum([seance.duree for seance in seances])
            data.append({
                'cours': cour.nom,
                'volume_horaire_total': cour.volume_horaire_total,
                'heures_effectuees': heures_effectuees,
            })
        return Response(data)

class DashboardDirecteurChefViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def progres_cours(self, request):
        user = request.user
        entite = user.profil.entite
        
        # Récupérer les cours associés à l'entité via les formations ou les classes
        cours_formations = Cours.objects.filter(formations__departement__entite=entite).distinct()
        data = []
        
        for cour in cours_formations:
            seances = Seance.objects.filter(cours=cour, statut='valide')
            heures_realisees = sum([seance.duree for seance in seances])
            progression = (heures_realisees / cour.volume_horaire_total) * 100 if cour.volume_horaire_total > 0 else 0
            data.append({
                'cours': cour.nom,
                'progression': progression
            })
        return Response(data)

    @action(detail=False, methods=['get'])
    def volume_heures_realisees(self, request):
        user = request.user
        entite = user.profil.entite
        
        # Récupérer les cours associés à l'entité via les formations ou les classes
        cours = Cours.objects.filter(formations__departement__entite=entite).distinct()
        data = []
        
        for cour in cours:
            seances = Seance.objects.filter(cours=cour, statut='valide')
            heures_realisees = sum([seance.duree for seance in seances])
            data.append({
                'cours': cour.nom,
                'heures_realisees': heures_realisees
            })
        return Response(data)

    @action(detail=False, methods=['get'])
    def etat_seances(self, request):
        user = request.user
        entite = user.profil.entite
        
        # Récupérer les séances associées à l'entité via les formations ou les classes
        seances = Seance.objects.filter(cours__formations__departement__entite=entite).distinct()
        
        data = {
            'total_seances': seances.count(),
            'seances_validees': seances.filter(statut='valide').count(),
            'seances_non_validees': seances.filter(statut='brouillon').count()
        }
        return Response(data)

class CoursViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all()
    serializer_class = CoursSerializer
    permission_classes = [IsAuthenticated, EstDirecteurAcademique]

    def get_queryset(self):
        user = self.request.user
        if user.profil.role == 'directeur_academique':
            return Cours.objects.filter(formations__departement__entite=user.profil.entite)
        return super().get_queryset()

class ClasseViewSet(viewsets.ModelViewSet):
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.profil.role == 'directeur_academique':
            return Classe.objects.filter(entite=user.profil.entite)
        

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cours
from classes.models import Classe
from formations.models import Formation
from django.db.models import Q

@login_required
def affecter_cours_formation(request, cours_id=None, formation_id=None):
    """Vue pour affecter un cours à une formation ou inversement"""
    if cours_id:
        cours = get_object_or_404(Cours, id=cours_id)
        if request.method == 'POST':
            formation_ids = request.POST.getlist('formations')
            cours.formations.set(formation_ids)
            messages.success(request, f"Le cours '{cours.nom}' a été affecté aux formations sélectionnées.")
            return redirect('detail_cours', cours_id=cours.id)
        
        formations = Formation.objects.all()
        return render(request, 'cours/affecter_cours_formation.html', {
            'cours': cours,
            'formations': formations,
            'formations_selectionnees': cours.formations.all(),
        })
    
    elif formation_id:
        formation = get_object_or_404(Formation, id=formation_id)
        if request.method == 'POST':
            cours_ids = request.POST.getlist('cours')
            for cours_id in cours_ids:
                cours = Cours.objects.get(id=cours_id)
                cours.formations.add(formation)
            
            messages.success(request, f"Les cours sélectionnés ont été affectés à la formation '{formation.nom}'.")
            return redirect('detail_formation', formation_id=formation.id)
        
        cours_disponibles = Cours.objects.all()
        return render(request, 'formations/affecter_cours.html', {
            'formation': formation,
            'cours_disponibles': cours_disponibles,
            'cours_selectionnes': formation.cours_disponibles.all(),
        })

@login_required
def affecter_cours_classe(request, cours_id=None, classe_id=None):
    """Vue pour affecter un cours à une classe ou inversement"""
    if cours_id:
        cours = get_object_or_404(Cours, id=cours_id)
        if request.method == 'POST':
            classe_ids = request.POST.getlist('classes')
            cours.classes.set(classe_ids)
            messages.success(request, f"Le cours '{cours.nom}' a été affecté aux classes sélectionnées.")
            return redirect('detail_cours', cours_id=cours.id)
        
        classes = Classe.objects.all()
        return render(request, 'cours/affecter_cours_classe.html', {
            'cours': cours,
            'classes': classes,
            'classes_selectionnees': cours.classes.all(),
        })
    
    elif classe_id:
        classe = get_object_or_404(Classe, id=classe_id)
        if request.method == 'POST':
            cours_ids = request.POST.getlist('cours')
            for cours_id in cours_ids:
                cours = Cours.objects.get(id=cours_id)
                cours.classes.add(classe)
            
            messages.success(request, f"Les cours sélectionnés ont été affectés à la classe '{classe.nom}'.")
            return redirect('detail_classe', classe_id=classe.id)
        
        cours_disponibles = Cours.objects.all()
        return render(request, 'classes/affecter_cours.html', {
            'classe': classe,
            'cours_disponibles': cours_disponibles,
            'cours_selectionnes': classe.cours.all(),
        })

@login_required
def affecter_classe_formation(request, classe_id=None, formation_id=None):
    """Vue pour affecter une classe à une formation ou inversement"""
    if classe_id:
        classe = get_object_or_404(Classe, id=classe_id)
        if request.method == 'POST':
            formation_ids = request.POST.getlist('formations')
            classe.formations.set(formation_ids)
            messages.success(request, f"La classe '{classe.nom}' a été affectée aux formations sélectionnées.")
            return redirect('detail_classe', classe_id=classe.id)
        
        formations = Formation.objects.all()
        return render(request, 'classes/affecter_classe_formation.html', {
            'classe': classe,
            'formations': formations,
            'formations_selectionnees': classe.formations.all(),
        })
    
    elif formation_id:
        formation = get_object_or_404(Formation, id=formation_id)
        if request.method == 'POST':
            classe_ids = request.POST.getlist('classes')
            for classe_id in classe_ids:
                classe = Classe.objects.get(id=classe_id)
                classe.formations.add(formation)
            
            messages.success(request, f"Les classes sélectionnées ont été affectées à la formation '{formation.nom}'.")
            return redirect('detail_formation', formation_id=formation.id)
        
        classes_disponibles = Classe.objects.all()
        return render(request, 'formations/affecter_classes.html', {
            'formation': formation,
            'classes_disponibles': classes_disponibles,
            'classes_selectionnees': formation.classes_associees.all(),
        })

@login_required
def recherche_cours(request):
    """Vue pour rechercher des cours selon différents critères"""
    query = request.GET.get('q', '')
    formation_id = request.GET.get('formation', '')
    classe_id = request.GET.get('classe', '')
    
    cours = Cours.objects.all()
    
    if query:
        cours = cours.filter(
            Q(nom__icontains=query) | 
            Q(code__icontains=query)
        )
    
    if formation_id:
        cours = cours.filter(formations__id=formation_id)
    
    if classe_id:
        cours = cours.filter(classes__id=classe_id)
    
    formations = Formation.objects.all()
    classes = Classe.objects.all()
    
    return render(request, 'cours/recherche_cours.html', {
        'cours': cours,
        'query': query,
        'formations': formations,
        'classes': classes,
        'formation_id': formation_id,
        'classe_id': classe_id,
    })