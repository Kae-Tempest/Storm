# apps/users/management/commands/seed_users.py
from django.core.management.base import BaseCommand
from apps.users.models import CustomUser
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Peuple la base de données avec des utilisateurs de test'

    def handle(self, *args, **options):
        usernames = ['alice', 'bob', 'charlie', 'david', 'emma', 'frank']
        bios = [
            "Développeur passionné 💻",
            "Fan de nouvelles technologies 🚀",
            "Toujours en train d'apprendre 📚",
            "Full-stack developer en devenir ⚡",
            "Aime coder et partager 🌟",
            "Explorateur du web moderne 🌐"
        ]

        users_created = []
        self.stdout.write('Création des utilisateurs...')

        for username in usernames:
            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'bio': random.choice(bios),
                    'date_of_birth': timezone.now() - timedelta(days=random.randint(8000, 20000))
                }
            )

            if created:
                user.set_password('password123')
                user.save()
                users_created.append(user)
                self.stdout.write(f'Créé: {username}')
            else:
                self.stdout.write(f'Existant: {username}')

        self.stdout.write(self.style.SUCCESS(f'{len(users_created)} nouveaux utilisateurs créés !'))