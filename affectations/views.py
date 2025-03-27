from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Affectation
from .serializers import AffectationSerializer
from .permissions import EstChefDepartementOuDirecteurAcademique

class AffectationViewSet(viewsets.ModelViewSet):
    queryset = Affectation.objects.all()
    serializer_class = AffectationSerializer
    permission_classes = [IsAuthenticated, EstChefDepartementOuDirecteurAcademique]