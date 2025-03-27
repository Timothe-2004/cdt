from django.contrib import admin
from django.urls import path, include
from .views import accueil  # Import de la vue accueil
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accueil, name='accueil'),  # Route pour la page d'accueil
    path('seances/', include('seances.urls', namespace='seances')),
    path('formations/', include('formations.urls', namespace='formations')),
    path('cours/', include('cours.urls', namespace='cours')),
    path('users/', include('users.urls', namespace='users')),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Ensure only one logout URL
]