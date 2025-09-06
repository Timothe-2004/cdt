from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router pour les API REST
router = DefaultRouter()
router.register(r'cours', views.CoursViewSet)
router.register(r'classes', views.ClasseViewSet)
router.register(r'dashboard-enseignant', views.DashboardEnseignantViewSet, basename='dashboard-enseignant')
router.register(r'dashboard-directeur-chef', views.DashboardDirecteurChefViewSet, basename='dashboard-directeur-chef')

app_name = 'cours'

urlpatterns = [
    path('', views.liste_cours, name='cours_home'),  # Redirige vers la liste des cours
    # URLs pour les vues basées sur les fonctions
    path('liste/', views.liste_cours, name='liste_cours'),
    path('detail/<int:cours_id>/', views.detail_cours, name='detail_cours'),
    path('cahier-texte/<int:cours_id>/', views.cahier_texte, name='cahier_texte'),
    path('ajouter/', views.ajouter_cours, name='ajouter_cours'),
    path('modifier/<int:cours_id>/', views.modifier_cours, name='modifier_cours'),
    path('supprimer/<int:cours_id>/', views.supprimer_cours, name='supprimer_cours'),  # Nouvelle URL
    
    # Nouvelles URLs pour la gestion des relations
    path('affecter-formation/<int:cours_id>/', views.affecter_cours_formation, name='affecter_cours_formation'),
    path('affecter-classe/<int:cours_id>/', views.affecter_cours_classe, name='affecter_cours_classe'),
    path('recherche/', views.recherche_cours, name='recherche_cours'),
    path('get_formations_by_departement/', views.get_formations_by_departement, name='get_formations_by_departement'),
    path('get_departments/', views.get_departments, name='get_departments'),
    path('get_classes_by_formation/', views.get_classes_by_formation, name='get_classes_by_formation'),
    # URLs pour l'API REST
    path('api/', include(router.urls)),
]