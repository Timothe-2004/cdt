from rest_framework import serializers
from .models import Classe

class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = ['id', 'nom', 'code', 'formations', 'annee_universitaire', 'effectif', 'entite_id']