from rest_framework import permissions
from rest_framework import serializers  # Ajout de l'importation manquante
from .models import Entite, Departement, ProfilUtilisateur, User  # Ajout de l'importation manquante pour User

class EstAdministrateur(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profil.role == 'administrateur'

class EstControleur(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profil.role == 'controleur'

class EstDirecteurAcademique(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profil.role == 'directeur_academique'

    def has_object_permission(self, request, view, obj):
        # Vérifie si l'objet appartient à l'entité du directeur académique
        if hasattr(obj, 'entite'):
            return obj.entite == request.user.profil.entite

        # Pour les classes, l'entité est accessible via la formation
        if hasattr(obj, 'formation') and hasattr(obj.formation, 'departement'):
            return obj.formation.departement.entite == request.user.profil.entite

        # Pour les départements
        if hasattr(obj, 'departement'):
            return obj.departement.entite == request.user.profil.entite

        return False

class EstChefDepartement(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profil.role == 'chef_departement'

    def has_object_permission(self, request, view, obj):
        # Limited to their own department
        if hasattr(obj, 'departement'):
            return obj.departement == request.user.profil.departement
        if hasattr(obj, 'formation') and hasattr(obj.formation, 'departement'):
            return obj.formation.departement == request.user.profil.departement
        return False

class DepartementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departement
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProfilUtilisateurSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProfilUtilisateur
        fields = '__all__'

class EstResponsableClasse(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profil.role == 'responsable_classe'

    def has_object_permission(self, request, view, obj):
        # Assigned to a specific class
        if hasattr(obj, 'classe'):
            return obj.classe.responsable == request.user
        return False

class EstEnseignant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profil.role == 'enseignant'

    def has_object_permission(self, request, view, obj):
        # Can validate sessions and is linked to a department
        if hasattr(obj, 'enseignant'):
            return obj.enseignant == request.user
        return False

class PeutValiderSeance(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profil.role == 'responsable_classe'

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'classe'):
            try:
                return obj.classe == request.user.responsabilite_classe.classe
            except:
                return False
        return False
