from rest_framework import permissions

class EstResponsableClasse(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profil.role == 'responsable_classe'

    def has_object_permission(self, request, view, obj):
        return obj.classe.responsable == request.user

class PeutValiderSeance(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profil.role == 'responsable_classe'

    def has_object_permission(self, request, view, obj):
        return obj.classe.responsable == request.user