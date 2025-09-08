#!/usr/bin/env python
"""
Script de chargement des données de test pour Render
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cahier_de_texte.settings")
    django.setup()
    
    print("📊 Chargement des données de test...")
    
    # Charger les données depuis data.json si le fichier existe
    if os.path.exists("data.json"):
        execute_from_command_line(["manage.py", "loaddata", "data.json"])
        print("✅ Données de test chargées !")
    else:
        print("ℹ️  Aucun fichier de données de test trouvé")
