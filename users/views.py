from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Entite, ProfilUtilisateur, Departement
from .forms import EntiteForm, AffecterDirecteurForm, DepartementForm
from classes.models import Classe
from classes.forms import ClasseForm
from formations.models import Formation
from cours.models import Cours
from users.permissions import EstDirecteurAcademique
from seances.models import Seance
from django.db.models import Q, F, Sum
from datetime import datetime

def is_directeur_academique(user):
    return user.profil.role == 'directeur_academique'

@login_required
def liste_utilisateurs(request):
    """Vue pour lister tous les utilisateurs."""
    utilisateurs = User.objects.all()
    return render(request, 'users/liste_utilisateurs.html', {'utilisateurs': utilisateurs})

@login_required
def creer_entite(request):
    """Vue pour créer une nouvelle entité."""
    if request.method == 'POST':
        form = EntiteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "L'entité a été créée avec succès.")
            return redirect('users:liste_entites')
    else:
        form = EntiteForm()
    return render(request, 'users/creer_entite.html', {'form': form})

@login_required
def affecter_directeur(request):
    """Vue pour affecter un directeur à une entité."""
    if request.method == 'POST':
        form = AffecterDirecteurForm(request.POST)
        if form.is_valid():
            directeur = form.cleaned_data['directeur']
            entite = form.cleaned_data['entite']
            profil, created = ProfilUtilisateur.objects.get_or_create(user=directeur)
            profil.role = 'directeur_academique'
            profil.entite = entite
            profil.save()
            messages.success(request, "Le directeur a été affecté avec succès.")
            return redirect('users:liste_entites')
    else:
        form = AffecterDirecteurForm()
    return render(request, 'users/affecter_directeur.html', {'form': form})

@login_required
def liste_entites(request):
    """Vue pour lister toutes les entités."""
    entites = Entite.objects.all()
    return render(request, 'users/liste_entites.html', {'entites': entites})

@login_required
@user_passes_test(is_directeur_academique)
def liste_departements(request):
    query = request.GET.get('q', '')
    departements = Departement.objects.filter(entite=request.user.profil.entite)

    if query:
        departements = departements.filter(
            Q(nom__icontains=query) | Q(code__icontains=query)
        )

    return render(request, 'users/liste_departements.html', {'departements': departements, 'query': query})

@login_required
@user_passes_test(is_directeur_academique)
def creer_departement(request):
    if request.method == 'POST':
        form = DepartementForm(request.POST, user=request.user)  # Pass the logged-in user to the form
        if form.is_valid():
            departement = form.save(commit=False)
            departement.entite = request.user.profil.entite  # Automatically set the 'entite' field
            departement.save()
            messages.success(request, 'Département créé avec succès!')
            return redirect('/users/departements/')
    else:
        form = DepartementForm(user=request.user)  # Pass the logged-in user to the form
    return render(request, 'users/creer_departement.html', {'form': form})

@login_required
@user_passes_test(is_directeur_academique)
def modifier_departement(request, departement_id):
    departement = get_object_or_404(Departement, id=departement_id)
    if request.method == 'POST':
        form = DepartementForm(request.POST, instance=departement)
        if form.is_valid():
            updated_departement = form.save(commit=False)
            # Vérifie que le département appartient à l'entité du directeur académique
            if updated_departement.entite != request.user.profil.entite:
                messages.error(request, "Vous ne pouvez pas modifier un département pour l'affecter à une entité différente de la vôtre.")
                return render(request, 'users/modifier_departement.html', {'form': form, 'departement': departement})
            updated_departement.save()
            messages.success(request, 'Département modifié avec succès!')
            return redirect('users:liste_departements')
    else:
        form = DepartementForm(instance=departement)
    return render(request, 'users/modifier_departement.html', {'form': form, 'departement': departement})

@login_required
@user_passes_test(is_directeur_academique)
def supprimer_departement(request, departement_id):
    departement = get_object_or_404(Departement, id=departement_id)
    if request.method == 'POST':
        departement.delete()
        messages.success(request, 'Département supprimé avec succès!')
        return redirect('users:liste_departements')
    return render(request, 'users/supprimer_departement.html', {'departement': departement})

@login_required
@user_passes_test(is_directeur_academique)
def liste_classes(request):
    classes = Classe.objects.filter(entite_id=request.user.profil.entite)
    return render(request, 'users/liste_classes.html', {'classes': classes})

@login_required
@user_passes_test(is_directeur_academique)
def creer_classe(request):
    departement_id = request.POST.get('departement')
    if request.method == 'POST':
        form = ClasseForm(request.POST, user=request.user, departement_id=departement_id)
        if form.is_valid():
            classe = form.save(commit=False)
            classe.entite_id = request.user.profil.entite  # Automatically set the entity
            classe.est_tronc_commun = form.cleaned_data['est_tronc_commun']  # Save the value of the radio button
            classe.save()
            messages.success(request, 'Classe créée avec succès!')
            return redirect('users:liste_classes')
    else:
        form = ClasseForm(user=request.user, departement_id=departement_id)
    return render(request, 'users/creer_classe.html', {'form': form})

@login_required
@user_passes_test(is_directeur_academique)
def affecter_responsable_classe(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    if request.method == 'POST':
        responsable_id = request.POST.get('responsable')
        responsable = get_object_or_404(User, id=responsable_id)

        # Validate that the selected user has the role 'responsable_classe'
        if not hasattr(responsable, 'profil') or responsable.profil.role != 'responsable_classe':
            messages.error(request, "L'utilisateur sélectionné n'a pas le rôle de responsable de classe.")
            return render(request, 'users/affecter_responsable_classe.html', {'classe': classe, 'utilisateurs': User.objects.filter(profil__role='responsable_classe')})

        classe.responsable = responsable
        classe.save()
        messages.success(request, 'Responsable de classe affecté avec succès!')
        return redirect('users:liste_classes')

    utilisateurs = User.objects.filter(profil__role='responsable_classe')
    return render(request, 'users/affecter_responsable_classe.html', {'classe': classe, 'utilisateurs': utilisateurs})

@login_required
@user_passes_test(is_directeur_academique)
def liste_formations(request):
    formations = Formation.objects.filter(departement__entite=request.user.profil.entite)
    return render(request, 'users/liste_formations.html', {'formations': formations})

@login_required
@user_passes_test(is_directeur_academique)
def liste_cours(request):
    cours = Cours.objects.filter(formations__departement__entite=request.user.profil.entite)
    return render(request, 'users/liste_cours.html', {'cours': cours})

@login_required
def dashboard(request):
    """Redirige les utilisateurs vers leur tableau de bord personnalisé."""
    user = request.user

    # Ajout de journaux pour déboguer le rôle
    print(f"Utilisateur connecté : {user.username}, Rôle : {user.profil.role}")

    if user.profil.role == 'administrateur':
        return render(request, 'users/dashboard_administrateur.html')
    elif user.profil.role == 'directeur_academique':
        return render(request, 'users/dashboard_directeur_academique.html')
    elif user.profil.role == 'enseignant':
        # Récupérer les cours affectés à l'enseignant
        cours = Cours.objects.filter(enseignant=user)
        return render(request, 'users/dashboard_enseignant.html', {'cours': cours})
    elif user.profil.role == 'responsable_classe':
        return redirect('seances:liste_seances')
    elif user.profil.role == 'controleur':
        # Récupérer toutes les classes
        classes = Classe.objects.all()

        # Récapitulatif des séances par enseignant
        from django.db.models import Count
        recapitulatif_seances = Seance.objects.values('enseignant__username').annotate(nb_seances=Count('id'))
        recapitulatif_seances_dict = {item['enseignant__username']: item['nb_seances'] for item in recapitulatif_seances}

        return render(request, 'users/dashboard_controleur.html', {
            'classes': classes,
            'recapitulatif_seances': recapitulatif_seances_dict
        })
    else:
        messages.error(request, "Votre rôle n'est pas reconnu. Veuillez contacter l'administrateur.")
        return redirect('accueil')

@login_required
def recapitulatif_par_enseignant(request):
    from django.db.models import Sum
    enseignants = Seance.objects.values('enseignant__id', 'enseignant__username', 'enseignant__first_name', 'enseignant__last_name').annotate(
        total_heures=Sum(
            (F('heure_fin__hour') * 60 + F('heure_fin__minute')) - (F('heure_debut__hour') * 60 + F('heure_debut__minute'))
        ) / 60.0  # Convertir les minutes en heures
    )
    return render(request, 'users/recapitulatif_par_enseignant.html', {
        'enseignants': enseignants
    })

@login_required
def details_seances_enseignant(request, enseignant_id):
    seances = Seance.objects.filter(enseignant_id=enseignant_id).select_related('cours', 'classe')

    # Calculer la durée pour chaque séance en heures
    for seance in seances:
        debut = datetime.combine(seance.date_seance, seance.heure_debut)
        fin = datetime.combine(seance.date_seance, seance.heure_fin)
        seance.duree = round((fin - debut).seconds / 3600, 2)  # Durée en heures avec 2 décimales

    return render(request, 'users/details_seances_enseignant.html', {
        'seances': seances
    })

@login_required
def cahier_de_texte_par_classe(request):
    classes = Classe.objects.all()
    return render(request, 'users/cahier_de_texte_par_classe.html', {
        'classes': classes
    })

@login_required
def seances_par_classe(request, classe_id):
    seances = Seance.objects.filter(classe_id=classe_id).select_related('cours', 'enseignant')
    classe = get_object_or_404(Classe, id=classe_id)

    # Calculer la durée pour chaque séance en heures
    for seance in seances:
        debut = datetime.combine(seance.date_seance, seance.heure_debut)
        fin = datetime.combine(seance.date_seance, seance.heure_fin)
        seance.duree = round((fin - debut).seconds / 3600, 2)  # Durée en heures avec 2 décimales

    return render(request, 'users/seances_par_classe.html', {
        'seances': seances,
        'classe': classe
    })

@login_required
def get_formations_by_departement(request):
    departement_id = request.GET.get('departement_id')
    if not departement_id:
        return JsonResponse({'error': 'No department ID provided'}, status=400)

    formations = Formation.objects.filter(departement_id=departement_id).values('id', 'nom')
    return JsonResponse(list(formations), safe=False)