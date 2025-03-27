from rest_framework import serializers
from .models import Affectation

class AffectationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affectation
        fields = '__all__'