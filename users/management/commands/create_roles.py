from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from cours.models import Cours
from formations.models import Formation, Departement
from seances.models import Seance
from classes.models import Classe

class Command(BaseCommand):
    help = 'Créer les rôles nécessaires pour le projet.'

    def handle(self, *args, **kwargs):
        roles = [
            'Administrateur',
            'Directeur académique',
            'Chef de département',
            'Enseignant',
            'Responsable de classe',
            'Contrôleur'
        ]

        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Rôle créé : {role}'))
            else:
                self.stdout.write(self.style.WARNING(f'Rôle déjà existant : {role}'))

        roles_permissions = {
            'Administrateur': Permission.objects.all(),
            'Directeur académique': Permission.objects.filter(codename__in=[
                'add_cours', 'change_cours', 'delete_cours', 'view_cours',
                'add_formation', 'change_formation', 'delete_formation', 'view_formation',
                'add_departement', 'change_departement', 'delete_departement', 'view_departement',
                'view_seance',
            ]),
            'Chef de département': Permission.objects.filter(codename__in=[
                'add_cours', 'change_cours', 'view_cours',
                'add_formation', 'change_formation', 'view_formation',
                'view_departement',
            ]),
            'Enseignant': Permission.objects.filter(codename__in=[
                'view_cours', 'view_formation', 'view_seance', 'change_seance',
            ]),
            'Responsable de classe': Permission.objects.filter(codename__in=[
                'view_seance', 'change_seance',
            ]),
            'Contrôleur': Permission.objects.filter(codename__in=[
                'view_cours', 'view_formation', 'view_seance',
            ]),
        }

        for role, permissions in roles_permissions.items():
            group, created = Group.objects.get_or_create(name=role)
            group.permissions.set(permissions)
            group.save()
            self.stdout.write(self.style.SUCCESS(f"Le groupe '{role}' a été créé avec succès."))