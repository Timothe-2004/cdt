from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Formation, Departement
from .serializers import FormationSerializer, DepartementSerializer
from classes.models import Classe
from cours.models import Cours

class FormationViewSet(ModelViewSet):
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer

class DepartementViewSet(ModelViewSet):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer

class ClasseViewSet(viewsets.ModelViewSet):
    queryset = Classe.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.profil.role == 'directeur_academique':
            return Classe.objects.filter(formation__departement__entite=user.profil.entite)
        return super().get_queryset()

class CoursViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.profil.role == 'directeur_academique':
            return Cours.objects.filter(formation__departement__entite=user.profil.entite)
        return super().get_queryset()