# views.py (reporting)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum
from cours.models import Cours
from seances.models import Seance
from formations.models import Formation
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CoursSerializer, SeanceSerializer, FormationSerializer
from users.permissions import EstControleur

def is_admin_or_chef(user):
    return user.is_superuser or hasattr(user, 'departement_dirige')

@login_required
@user_passes_test(is_admin_or_chef)
def statistiques(request):
    total_formations = Formation.objects.count()
    total_cours = Cours.objects.count()
    total_seances = Seance.objects.count()

    # Statistiques de progression
    cours_stats = Cours.objects.annotate(
        nb_seances=Count('seances'),
        heures_realisees=Sum('seances__duree')
    )

    # Formations par département
    formations_par_departement = Formation.objects.values('departement__nom').annotate(
        count=Count('id')
    ).order_by('departement__nom')

    context = {
        'total_formations': total_formations,
        'total_cours': total_cours,
        'total_seances': total_seances,
        'cours_stats': cours_stats,
        'formations_par_departement': formations_par_departement,
    }

    return render(request, 'reporting/statistiques.html', context)

class ReportingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, EstControleur]

    @action(detail=False, methods=['get'])
    def cours(self, request):
        cours = Cours.objects.all()
        serializer = CoursSerializer(cours, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def seances(self, request):
        seances = Seance.objects.all()
        serializer = SeanceSerializer(seances, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def formations(self, request):
        formations = Formation.objects.all()
        serializer = FormationSerializer(formations, many=True)
        return Response(serializer.data)