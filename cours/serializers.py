from rest_framework import serializers
from cours.models import Cours
from classes.models import Classe
from formations.models import Formation
from seances.models import Seance
from users.serializers import UserSerializer

class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = '__all__'

class ClasseSerializer(serializers.ModelSerializer):
    formations = FormationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Classe
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['formations'] = FormationSerializer(instance.formations.all(), many=True).data
        return representation

class CoursSerializer(serializers.ModelSerializer):
    formations = FormationSerializer(many=True, read_only=True)
    classes = ClasseSerializer(many=True, read_only=True)
    enseignant = UserSerializer(read_only=True)
    
    class Meta:
        model = Cours
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['formations'] = FormationSerializer(instance.formations.all(), many=True).data
        representation['classes'] = ClasseSerializer(instance.classes.all(), many=True).data
        if instance.enseignant:
            representation['enseignant'] = UserSerializer(instance.enseignant).data
        return representation

class SeanceSerializer(serializers.ModelSerializer):
    cours = CoursSerializer(read_only=True)
    
    class Meta:
        model = Seance
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['cours'] = CoursSerializer(instance.cours).data
        return representation