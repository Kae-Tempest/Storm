# apps/posts/management/commands/seed_posts.py
from django.core.management.base import BaseCommand
from apps.users.models import CustomUser
from apps.posts.models import Post
import random
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Peuple la base de données avec des posts de test'

    def handle(self, *args, **options):
        # Nettoyage des tables existantes
        self.stdout.write('Nettoyage des tables existantes...')
        # Cette ligne va aussi nettoyer la table post_likes à cause de la relation CASCADE
        Post.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Tables nettoyées !'))

        # Vérification des utilisateurs existants
        users = list(CustomUser.objects.all())
        if not users:
            self.stdout.write(
                self.style.ERROR('Aucun utilisateur trouvé. Veuillez d\'abord exécuter python manage.py seed_users'))
            return

        # Contenus de posts avec des hashtags et des emojis
        sample_contents = [
            "Je découvre Django Ninja avec SvelteKit ! 🚀 #Django #Svelte",
            "La stack moderne c'est quelque chose 💪 #WebDev",
            "Les API REST c'est la vie 🌐 #API #Backend",
            "Je viens de terminer mon premier projet fullstack ✨ #FullStack",
            "Le TypeScript c'est vraiment top 💎 #TypeScript",
            "Docker c'est magique quand ça marche 🐳 #Docker #DevOps",
            "J'adore travailler avec PostgreSQL 🐘 #Database",
            "Les migrations Django c'est pratique 🔄 #Django",
            "Le dev web en 2025 c'est fou 🚀 #Future #WebDev",
            "Je commence à comprendre les WebSockets 🔌 #RealTime",
            "L'architecture microservices c'est intéressant 🏗️ #Architecture",
            "Je teste le nouveau framework Storm 🌪️ #Innovation",
            "L'authentification avec JWT c'est puissant 🔐 #Security",
            "Les tests automatisés sauvent des vies 🧪 #Testing",
            "Le déploiement continu c'est la clé 🔑 #CI/CD"
        ]

        self.stdout.write('Création des posts...')
        posts_created = []

        # Création des posts
        for i in range(30):  # Création de 30 posts
            post = Post.objects.create(
                content=random.choice(sample_contents),
                author=random.choice(users),
                created_at=timezone.now() - timedelta(
                    days=random.randint(0, 30),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
            )

            # Ajout de likes aléatoires (entre 0 et 60% des utilisateurs)
            num_likes = random.randint(0, int(len(users) * 0.6))
            liking_users = random.sample(users, num_likes)
            post.likes.set(liking_users)

            posts_created.append(post)
            self.stdout.write(f'Post {i + 1}/30 créé avec {num_likes} likes')

        self.stdout.write(self.style.SUCCESS(f'{len(posts_created)} posts créés avec succès !'))