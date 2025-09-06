from users.permissions import EstDirecteurAcademique
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import render

class ClasseViewSet(viewsets.ModelViewSet):
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer
    permission_classes = [IsAuthenticated, EstDirecteurAcademique]

    def get_queryset(self):
        user = self.request.user
        if user.profil.role == 'directeur_academique':
            return Classe.objects.filter(departement__entite=user.profil.entite)
        return super().get_queryset()

@login_required
@user_passes_test(is_directeur_academique)
def liste_classes(request):
    query = request.GET.get('q', '')
    classes = Classe.objects.filter(entite=request.user.profil.entite)

    if query:
        classes = classes.filter(
            Q(nom__icontains=query) | Q(code__icontains=query)
        )

    return render(request, 'classes/liste_classes.html', {'classes': classes, 'query': query})