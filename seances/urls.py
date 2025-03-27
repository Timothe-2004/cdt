# urls.py (seances)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SeanceViewSet, HistoriqueValidationViewSet, DashboardResponsableClasseViewSet
from . import views

router = DefaultRouter()
router.register(r'seances', SeanceViewSet)
router.register(r'historique-validations', HistoriqueValidationViewSet)
router.register(r'dashboard-responsable', DashboardResponsableClasseViewSet, basename='dashboard-responsable')

app_name = 'seances'

urlpatterns = [
    path('', include(router.urls)),
    path('liste/', views.liste_seances, name='liste_seances'),  # Définir la route pour liste_seances
    path('<int:seance_id>/', views.detail_seance, name='detail_seance'),  # Route pour le détail d'une séance
    path('ajouter/', views.ajouter_seance, name='ajouter_seance'),  # Route pour ajouter une séance
]
