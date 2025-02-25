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
                "media_url": "https://images.unsplash.com/photo-1587620962725-abab7fe55159?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            },
            {
                "title": "La Stack Moderne",
                "content": "La stack moderne c'est quelque chose 💪 #WebDev",
                "location": "Lyon, France",
                "media_url": "https://images.unsplash.com/photo-1581276879432-15e50529f34b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            },
            {
                "title": "API REST",
                "content": "Les API REST c'est la vie 🌐 #API #Backend",
                "location": "Marseille, France",
                "media_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            },
            {
                "title": "Premier Projet Fullstack",
                "content": "Je viens de terminer mon premier projet fullstack ✨ #FullStack",
                "location": "Bordeaux, France",
                "media_url": "https://images.unsplash.com/photo-1607706189992-eae578626c86?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            },
            {
                "title": "TypeScript Daily",
                "content": "Le TypeScript c'est vraiment top 💎 #TypeScript",
                "location": "Toulouse, France",
                "media_url": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            },
            {
                "title": "Docker en Production",
                "content": "Docker c'est magique quand ça marche 🐳 #Docker #DevOps",
                "location": "Nantes, France",
                "media_url": "https://images.unsplash.com/photo-1605745341112-85968b19335b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            },
            {
                "title": "PostgreSQL Performance",
                "content": "J'adore travailler avec PostgreSQL 🐘 #Database",
                "location": "Lille, France",
                "media_url": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            },
            {
                "title": "Migrations Django",
                "content": "Les migrations Django c'est pratique 🔄 #Django",
                "location": "Strasbourg, France",
                "media_url": "https://images.unsplash.com/photo-1603468620905-8de7d86b781e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            },
            {
                "title": "Web Dev 2025",
                "content": "Le dev web en 2025 c'est fou 🚀 #Future #WebDev",
                "location": "Nice, France",
                "media_url": "https://images.unsplash.com/photo-1516116216624-53e697fedbea?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            },
            {
                "title": "WebSockets en Action",
                "content": "Je commence à comprendre les WebSockets 🔌 #RealTime",
                "location": "Rennes, France",
                "media_url": "https://images.unsplash.com/photo-1534972195531-d756b9bfa9f2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            },
            {
                "title": "Architecture Microservices",
                "content": "L'architecture microservices c'est intéressant 🏗️ #Architecture",
                "location": "Montpellier, France",
                "media_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            },
            {
                "title": "Framework Storm",
                "content": "Je teste le nouveau framework Storm 🌪️ #Innovation",
                "location": "Grenoble, France",
                "media_url": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            },
            {
                "title": "Sécurité JWT",
                "content": "L'authentification avec JWT c'est puissant 🔐 #Security",
                "location": "Dijon, France",
                "media_url": "https://images.unsplash.com/photo-1560807707-8cc77767d783?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            },
            {
                "title": "Tests Automatisés",
                "content": "Les tests automatisés sauvent des vies 🧪 #Testing",
                "location": "Angers, France",
                "media_url": "https://images.unsplash.com/photo-1532094349884-543bc11b234d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            },
            {
                "title": "CI/CD Pipeline",
                "content": "Le déploiement continu c'est la clé 🔑 #CI/CD",
                "location": "Reims, France",
                "media_url": "https://images.unsplash.com/photo-1555099962-4199c345e5dd?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
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
