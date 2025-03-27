from rest_framework import serializers
from .models import Seance, HistoriqueValidation

class SeanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seance
        fields = '__all__'

class HistoriqueValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriqueValidation
        fields = '__all__'