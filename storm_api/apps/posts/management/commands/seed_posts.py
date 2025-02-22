# apps/posts/management/commands/seed_posts.py
import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.posts.models import Post
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Peuple la base de données avec des posts de test"

    def handle(self, *args, **options):
        # Nettoyage des tables existantes
        self.stdout.write("Nettoyage des tables existantes...")
        Post.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Tables nettoyées !"))

        # Vérification des utilisateurs existants
        users = list(CustomUser.objects.all())
        if not users:
            self.stdout.write(
                self.style.ERROR(
                    "Aucun utilisateur trouvé. Veuillez d'abord exécuter python manage.py seed_users"
                )
            )
            return

        # Sample data for posts
        sample_data = [
            {
                "title": "Découverte de Django Ninja",
                "content": "Je découvre Django Ninja avec SvelteKit ! 🚀 #Django #Svelte",
                "location": "Paris, France",
                "media_url": "https://example.com/images/django-ninja.jpg",
            },
            {
                "title": "La Stack Moderne",
                "content": "La stack moderne c'est quelque chose 💪 #WebDev",
                "location": "Lyon, France",
                "media_url": "https://example.com/images/modern-stack.jpg",
            },
            {
                "title": "API REST",
                "content": "Les API REST c'est la vie 🌐 #API #Backend",
                "location": "Marseille, France",
                "media_url": "https://example.com/images/api-rest.jpg",
            },
            {
                "title": "Premier Projet Fullstack",
                "content": "Je viens de terminer mon premier projet fullstack ✨ #FullStack",
                "location": "Bordeaux, France",
                "media_url": "https://example.com/images/fullstack.jpg",
            },
            {
                "title": "TypeScript Daily",
                "content": "Le TypeScript c'est vraiment top 💎 #TypeScript",
                "location": "Toulouse, France",
                "media_url": "https://example.com/images/typescript.jpg",
            },
            {
                "title": "Docker en Production",
                "content": "Docker c'est magique quand ça marche 🐳 #Docker #DevOps",
                "location": "Nantes, France",
                "media_url": "https://example.com/images/docker.jpg",
            },
            {
                "title": "PostgreSQL Performance",
                "content": "J'adore travailler avec PostgreSQL 🐘 #Database",
                "location": "Lille, France",
                "media_url": "https://example.com/images/postgresql.jpg",
            },
            {
                "title": "Migrations Django",
                "content": "Les migrations Django c'est pratique 🔄 #Django",
                "location": "Strasbourg, France",
                "media_url": "https://example.com/images/django-migrations.jpg",
            },
            {
                "title": "Web Dev 2025",
                "content": "Le dev web en 2025 c'est fou 🚀 #Future #WebDev",
                "location": "Nice, France",
                "media_url": "https://example.com/images/webdev-2025.jpg",
            },
            {
                "title": "WebSockets en Action",
                "content": "Je commence à comprendre les WebSockets 🔌 #RealTime",
                "location": "Rennes, France",
                "media_url": "https://example.com/images/websockets.jpg",
            },
            {
                "title": "Architecture Microservices",
                "content": "L'architecture microservices c'est intéressant 🏗️ #Architecture",
                "location": "Montpellier, France",
                "media_url": "https://example.com/images/microservices.jpg",
            },
            {
                "title": "Framework Storm",
                "content": "Je teste le nouveau framework Storm 🌪️ #Innovation",
                "location": "Grenoble, France",
                "media_url": "https://example.com/images/storm-framework.jpg",
            },
            {
                "title": "Sécurité JWT",
                "content": "L'authentification avec JWT c'est puissant 🔐 #Security",
                "location": "Dijon, France",
                "media_url": "https://example.com/images/jwt-auth.jpg",
            },
            {
                "title": "Tests Automatisés",
                "content": "Les tests automatisés sauvent des vies 🧪 #Testing",
                "location": "Angers, France",
                "media_url": "https://example.com/images/automated-tests.jpg",
            },
            {
                "title": "CI/CD Pipeline",
                "content": "Le déploiement continu c'est la clé 🔑 #CI/CD",
                "location": "Reims, France",
                "media_url": "https://example.com/images/cicd.jpg",
            },
        ]

        self.stdout.write("Création des posts...")
        posts_created = []

        # Création des posts
        for i in range(30):  # Création de 30 posts
            sample = random.choice(sample_data)
            post = Post.objects.create(
                title=sample["title"],
                content=sample["content"],
                media_url=sample["media_url"],
                location=sample["location"],
                author=random.choice(users),
                created_at=timezone.now()
                           - timedelta(
                    days=random.randint(0, 30),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59),
                ),
            )

            # Ajout de likes aléatoires (entre 0 et 60% des utilisateurs)
            num_likes = random.randint(0, int(len(users) * 0.6))
            liking_users = random.sample(users, num_likes)
            post.likes.set(liking_users)

            posts_created.append(post)
            self.stdout.write(f"Post {i + 1}/30 créé avec {num_likes} likes")

        self.stdout.write(
            self.style.SUCCESS(f"{len(posts_created)} posts créés avec succès !")
        )
