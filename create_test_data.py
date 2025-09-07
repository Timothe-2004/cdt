#!/usr/bin/env python
"""
Script de création de données de test pour SQLite
"""
import os
import sys
import django
from django.contrib.auth import get_user_model
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cahier_de_texte.settings")
    django.setup()
    
    User = get_user_model()
    
    print("📊 Création des données de test...")
    
    # Créer des utilisateurs de test
    try:
        # Créer un enseignant
        if not User.objects.filter(username='enseignant1').exists():
            user = User.objects.create_user(
                username='enseignant1',
                email='enseignant1@example.com',
                password='enseignant123',
                first_name='Jean',
                last_name='Dupont'
            )
            # Créer le profil enseignant
            from users.models import Profil
            Profil.objects.create(
                user=user,
                role='enseignant',
                telephone='0123456789'
            )
            print("✅ Enseignant créé: enseignant1/enseignant123")
        
        # Créer un administrateur
        if not User.objects.filter(username='admin2').exists():
            user = User.objects.create_user(
                username='admin2',
                email='admin2@example.com',
                password='admin123',
                first_name='Marie',
                last_name='Martin'
            )
            # Créer le profil administrateur
            from users.models import Profil
            Profil.objects.create(
                user=user,
                role='administrateur',
                telephone='0987654321'
            )
            print("✅ Administrateur créé: admin2/admin123")
        
        print("✅ Données de test créées avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données: {e}")
        print("ℹ️  Assurez-vous que les modèles sont correctement définis")
