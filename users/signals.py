from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission
from .models import ProfilUtilisateur, Entite

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Check if a ProfilUtilisateur already exists for the user
        if not hasattr(instance, 'profil'):
            if instance.is_superuser or instance.groups.filter(name='contrôleur').exists():
                ProfilUtilisateur.objects.create(user=instance, role='administrateur' if instance.is_superuser else 'contrôleur')
            else:
                entite = Entite.objects.first()  # Assurez-vous qu'il y a au moins une entité dans la base de données
                if entite:
                    ProfilUtilisateur.objects.create(user=instance, role='enseignant', entite=entite)
                else:
                    ProfilUtilisateur.objects.create(user=instance, role='enseignant')

@receiver(post_save, sender=ProfilUtilisateur)
def assign_user_group(sender, instance, created, **kwargs):
    # Assigner les permissions au groupe
    group_name = instance.role
    group, created = Group.objects.get_or_create(name=group_name)

    if group_name == 'administrateur':
        permissions = Permission.objects.all()
    elif group_name == 'contrôleur':
        permissions = Permission.objects.filter(codename__in=[
            'view_seance', 'view_cours', 'view_formation'
        ])
    elif group_name == 'directeur_académique':
        permissions = Permission.objects.filter(codename__in=[
            'add_cours', 'change_cours', 'delete_cours', 'view_cours',
            'add_seance', 'change_seance', 'delete_seance', 'view_seance',
            'add_formation', 'change_formation', 'delete_formation', 'view_formation',
            'add_departement', 'change_departement', 'delete_departement', 'view_departement'
        ])
    elif group_name == 'chef_departement':
        permissions = Permission.objects.filter(codename__in=[
            'add_cours', 'change_cours', 'delete_cours', 'view_cours',
            'add_seance', 'change_seance', 'delete_seance', 'view_seance',
            'add_formation', 'change_formation', 'delete_formation', 'view_formation',
            'add_classe', 'change_classe', 'delete_classe', 'view_classe'
        ])
    elif group_name == 'enseignant':
        permissions = Permission.objects.filter(codename__in=[
            'add_seance', 'change_seance', 'view_seance',
            'view_cours', 'view_formation'
        ])
    elif group_name == 'responsable_classe':
        permissions = Permission.objects.filter(codename__in=[
            'add_seance', 'change_seance', 'view_seance',
            'view_cours', 'view_formation'
        ])
    else:
        # Cas par défaut : aucune permission
        permissions = Permission.objects.none()

    group.permissions.set(permissions)
    instance.user.groups.add(group)
