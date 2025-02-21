# core/automigrations.py
import os

import django
from django.core.management import call_command


def run_migrations() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    django.setup()

    try:
        # Vérifier et créer les migrations si nécessaire
        print("Vérification des migrations manquantes...")
        call_command("makemigrations", "users", verbosity=1)
        call_command("makemigrations", "posts", verbosity=1)
        call_command("makemigrations", "comments", verbosity=1)

        # Migrer les applications dans l'ordre correct
        print("\nApplication des migrations...")

        # 1. Migrer d'abord le contenu de base
        call_command("migrate", "contenttypes", verbosity=1)

        # 2. Créer la table 'users' avant toute dépendance
        call_command("migrate", "users", verbosity=1)

        # 3. Puis auth qui pourrait dépendre de users
        call_command("migrate", "auth", verbosity=1)

        # 4. Puis les autres applications qui peuvent dépendre des utilisateurs
        call_command("migrate", "posts", verbosity=1)
        call_command("migrate", "comments", verbosity=1)
        call_command("migrate", "authentication", verbosity=1)

        # 5. Enfin, les applications Django restantes
        call_command("migrate", "admin", verbosity=1)
        call_command("migrate", "sessions", verbosity=1)
        call_command("migrate", "messages", verbosity=1)
        call_command("migrate", "staticfiles", verbosity=1)

        print("Migrations automatiques terminées avec succès.")

    except Exception as e:
        print(f"Erreur pendant les migrations: {e}")
