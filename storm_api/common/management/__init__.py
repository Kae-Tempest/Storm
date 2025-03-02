from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Peuple la base de données avec des utilisateurs et des posts de test'

    def handle(self, *args, **options):
        self.stdout.write('Début du peuplement de la base de données...')

        self.stdout.write('\n1. Création des utilisateurs...')
        call_command('seed_users')

        self.stdout.write('\n2. Création des posts...')
        call_command('seed_posts')

        self.stdout.write(self.style.SUCCESS('\nBase de données peuplée avec succès !'))