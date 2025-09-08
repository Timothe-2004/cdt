#!/usr/bin/env python
"""
Script de création de superutilisateur pour Render
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
    
    # Vérifier si un superutilisateur existe déjà
    if User.objects.filter(is_superuser=True).exists():
        print("✅ Un superutilisateur existe déjà")
    else:
        print("👤 Création d'un superutilisateur...")
        execute_from_command_line(["manage.py", "createsuperuser", "--noinput"])
        print("✅ Superutilisateur créé !")
