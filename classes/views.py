from users.permissions import EstDirecteurAcademique

class ClasseViewSet(viewsets.ModelViewSet):
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer
    permission_classes = [IsAuthenticated, EstDirecteurAcademique]

    def get_queryset(self):
        user = self.request.user
        if user.profil.role == 'directeur_academique':
            return Classe.objects.filter(departement__entite=user.profil.entite)
        return super().get_queryset()