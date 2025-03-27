from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FormationViewSet, liste_formations, detail_formation, ajouter_formation, ClasseViewSet, CoursViewSet, modifier_formation

app_name = 'formations'

# Configuration du routeur pour les API REST
router = DefaultRouter()
router.register(r'formations', FormationViewSet, basename='formation')
router.register(r'classes', ClasseViewSet, basename='classe')
router.register(r'cours', CoursViewSet, basename='cours')

# Définition des URL pour les vues basées sur des fonctions
urlpatterns = [
    path('', liste_formations, name='liste_formations'),
    path('<int:formation_id>/', detail_formation, name='detail_formation'),
    path('ajouter/', ajouter_formation, name='ajouter_formation'),
    path('<int:formation_id>/modifier/', modifier_formation, name='modifier_formation'),
]

# Ajout des routes du routeur
urlpatterns += router.urls
