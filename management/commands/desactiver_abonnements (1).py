import os
import sys

# Ajouter le chemin du projet au sys.path
sys.path.append('/home/geraldehako/Mondjai')

# Définir la variable d'environnement DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Prologicielsucces.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from Gestions.models import Abonnement
# Importation de BaseCommand
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Désactive les abonnements dont la date de fin est dépassée'

    def handle(self, *args, **kwargs):
        Abonnement.desactiver_abonnements_expired()
        self.stdout.write(self.style.SUCCESS('Abonnements expirés désactivés avec succès.'))