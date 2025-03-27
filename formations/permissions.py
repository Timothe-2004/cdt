from rest_framework import permissions

class EstDirecteurAcademique(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profil.role == 'directeur_academique'
    
    def has_object_permission(self, request, view, obj):
        # Vérifier si l'objet appartient à l'entité du directeur
        if hasattr(obj, 'entite'):
            return obj.entite == request.user.profil.entite
        
        # Pour les classes, l'entité est accessible via la formation
        if hasattr(obj, 'formation') and hasattr(obj.formation, 'entite'):
            return obj.formation.entite == request.user.profil.entite
        
        return False