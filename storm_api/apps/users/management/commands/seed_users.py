import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Peuple la base de données avec des utilisateurs de test"

    def handle(self, *args, **options):
        # Nettoyage des utilisateurs existants
        self.stdout.write("Nettoyage des users existants...")
        CustomUser.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Users nettoyés !"))

        usernames = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank"]
        bios = [
            "Développeur passionné 💻",
            "Fan de nouvelles technologies 🚀",
            "Toujours en train d'apprendre 📚",
            "Full-stack developer en devenir ⚡",
            "Aime coder et partager 🌟",
            "Explorateur du web moderne 🌐",
        ]

        users_created = []
        self.stdout.write("Création des utilisateurs...")

        for username in usernames:
            # Création d'un tag_name unique basé sur le username
            display_name = f"{username}".lower()

            try:
                user = CustomUser.objects.create(
                    username=username,
                    email=f"{username}@example.com",
                    display_name=display_name,
                    bio=random.choice(bios),
                    date_of_birth=timezone.now().date()
                                  - timedelta(days=random.randint(8000, 20000)),
                    is_active=True,
                    is_staff=random.choice([True, False]),
                )

                user.set_password("password123")
                user.save()
                users_created.append(user)
                self.stdout.write(f"Créé: {username} (tag: {display_name})")

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Erreur lors de la création de {username}: {str(e)}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(f"{len(users_created)} nouveaux utilisateurs créés !")
        )
