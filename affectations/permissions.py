from rest_framework import permissions

class EstChefDepartementOuDirecteurAcademique(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.profil.role == 'chef_departement' or
            request.user.profil.role == 'directeur_academique'
        )