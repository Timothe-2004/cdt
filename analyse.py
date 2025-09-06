import os
import django
import io
from django.core.management import call_command

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cahier_de_texte.settings')
django.setup()

# Export des données
with io.open('data.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 
                 indent=4, 
                 stdout=f, 
                 use_natural_primary_keys=True, 
                 use_natural_foreign_keys=True)
