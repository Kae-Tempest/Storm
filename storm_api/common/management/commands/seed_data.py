from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Peuple la base de données avec des utilisateurs et des posts de test"

    def handle(self, *args, **options) -> None:
        self.stdout.write("Début du peuplement de la base de données...")

        self.stdout.write("\n1. Création des utilisateurs...")
        call_command("seed_users")

        self.stdout.write("\n2. Création des posts...")
        call_command("seed_posts")

        self.stdout.write("\n3. Création des commentaires...")
        call_command("seed_comments")

        self.stdout.write(self.style.SUCCESS("\nBase de données peuplée avec succès !"))
