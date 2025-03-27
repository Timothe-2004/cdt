from django.urls import path, include
from .views import liste_utilisateurs, creer_entite, affecter_directeur, liste_entites, dashboard
from . import views

app_name = 'users'

urlpatterns = [
    path('liste-utilisateurs/', liste_utilisateurs, name='liste_utilisateurs'),
    path('creer-entite/', creer_entite, name='creer_entite'),
    path('affecter-directeur/', affecter_directeur, name='affecter_directeur'),
    path('liste-entites/', liste_entites, name='liste_entites'),
    path('departements/', views.liste_departements, name='liste_departements'),
    path('departements/creer/', views.creer_departement, name='creer_departement'),
    path('departements/<int:departement_id>/modifier/', views.modifier_departement, name='modifier_departement'),
    path('departements/<int:departement_id>/supprimer/', views.supprimer_departement, name='supprimer_departement'),
    path('dashboard/', dashboard, name='dashboard'),
    path('classes/', views.liste_classes, name='liste_classes'),
    path('classes/creer/', views.creer_classe, name='creer_classe'),
    path('classes/<int:classe_id>/affecter-responsable/', views.affecter_responsable_classe, name='affecter_responsable_classe'),
]