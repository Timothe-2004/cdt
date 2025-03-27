from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Departement
from .models import Entite
from .models import ProfilUtilisateur

# Étendre l'admin utilisateur pour inclure les rôles
class ProfilUtilisateurInline(admin.StackedInline):
    model = ProfilUtilisateur
    can_delete = False
    verbose_name_plural = 'Profil Utilisateur'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfilUtilisateurInline,)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Logique pour attribuer les rôles spécifiques
        if hasattr(obj, 'profil'):
            if obj.username in ['directeur', 'directeurA']:
                obj.profil.role = 'directeur_academique'
            elif obj.username == 'responsable':
                obj.profil.role = 'responsable_classe'
            obj.profil.save()

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Suppression de l'enregistrement du modèle Departement dans l'interface admin
# @admin.register(Departement)
# class DepartementAdmin(admin.ModelAdmin):
#     list_display = ('nom', 'code', 'entite', 'date_creation')
#     search_fields = ('nom', 'code')
#     list_filter = ('entite',)

@admin.register(Entite)
class EntiteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'description', 'date_creation')
    search_fields = ('nom', 'code')
    list_filter = ('date_creation',)

    def save_model(self, request, obj, form, change):
        """Personnalisation de la sauvegarde pour gérer les directeurs adjoints."""
        super().save_model(request, obj, form, change)
        # Logique pour affecter des directeurs adjoints si nécessaire
        # Exemple : obj.directeur_adjoint = ...
