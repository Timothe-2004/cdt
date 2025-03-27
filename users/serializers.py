from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Entite, Departement, ProfilUtilisateur
from classes.models import ResponsableClasse
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EntiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entite
        fields = '__all__'

class DepartementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departement
        fields = '__all__'

class ProfilUtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilUtilisateur
        fields = '__all__'

class ResponsableClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsableClasse
        fields = '__all__'
