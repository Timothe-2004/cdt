#!/usr/bin/env python
"""
Script de migration automatique pour Render
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cahier_de_texte.settings")
    django.setup()
    
    print("🔄 Exécution des migrations...")
    execute_from_command_line(["manage.py", "migrate"])
    
    print("✅ Migrations terminées !")
