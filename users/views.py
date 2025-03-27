from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Entite, ProfilUtilisateur, Departement
from .forms import EntiteForm, AffecterDirecteurForm, DepartementForm
from classes.models import Classe
from classes.forms import ClasseForm
from formations.models import Formation
from cours.models import Cours
from users.permissions import EstDirecteurAcademique

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
@user_passes_test(lambda u: u.profil.role == 'directeur_academique')
def liste_departements(request):
    departements = Departement.objects.filter(entite=request.user.profil.entite)
    return render(request, 'users/liste_departements.html', {'departements': departements})

@login_required
@user_passes_test(is_directeur_academique)
def creer_departement(request):
    if request.method == 'POST':
        form = DepartementForm(request.POST)
        if form.is_valid():
            departement = form.save(commit=False)
            # Vérifie que le département appartient à l'entité du directeur académique
            if departement.entite != request.user.profil.entite:
                messages.error(request, "Vous ne pouvez pas créer un département pour une entité différente de la vôtre.")
                return render(request, 'users/creer_departement.html', {'form': form})
            departement.save()
            messages.success(request, 'Département créé avec succès!')
            return redirect('/users/departements/')  # Redirection explicite vers la page souhaitée
    else:
        form = DepartementForm()
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
    if request.method == 'POST':
        form = ClasseForm(request.POST)
        if form.is_valid():
            classe = form.save(commit=False)
            classe.departement = request.user.profil.entite.departements.first()
            classe.save()
            messages.success(request, 'Classe créée avec succès!')
            return redirect('users:liste_classes')
    else:
        form = ClasseForm()
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
        return render(request, 'users/dashboard_responsable_classe.html')
    elif user.profil.role == 'controleur':
        return render(request, 'users/dashboard_controleur.html')
    else:
        messages.error(request, "Votre rôle n'est pas reconnu. Veuillez contacter l'administrateur.")
        return redirect('accueil')