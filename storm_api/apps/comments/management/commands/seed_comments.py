import random
from datetime import timedelta

from apps.comments.models import Comment
from apps.posts.models import Post
from apps.users.models import CustomUser
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Peuple la base de données avec des commentaires de test"

    def handle(self, *args, **options):
        # Nettoyage des commentaires existants
        self.stdout.write("Nettoyage des commentaires existants...")
        Comment.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Commentaires nettoyés !"))

        # Vérification des posts et utilisateurs existants
        posts = list(Post.objects.all())
        users = list(CustomUser.objects.all())

        if not posts:
            self.stdout.write(
                self.style.ERROR(
                    "Aucun post trouvé. Veuillez d'abord exécuter python manage.py seed_posts"
                )
            )
            return

        if not users:
            self.stdout.write(
                self.style.ERROR(
                    "Aucun utilisateur trouvé. Veuillez d'abord exécuter python manage.py seed_users"
                )
            )
            return

        # Exemples de commentaires
        sample_comments = [
            "Totalement d'accord ! 👍",
            "Super article, merci pour le partage 🙏",
            "C'est très intéressant 🤔",
            "Je n'avais pas vu ça sous cet angle 🎯",
            "On pourrait approfondir ce sujet 💭",
            "Excellent point de vue 🌟",
            "Ça me donne envie d'essayer 🚀",
            "Belle analyse 📊",
            "Je partage ton opinion 🤝",
            "C'est exactement ce que je cherchais 🎉",
            "Merci pour ces précisions 📝",
            "Très pertinent 💡",
            "Je vais tester ça 🛠️",
            "Bien expliqué ! ✨",
            "C'est noté 📌",
        ]

        self.stdout.write("Création des commentaires...")
        comments_created = 0

        # Pour chaque post, créer entre 0 et 10 commentaires
        for post in posts:
            num_comments = random.randint(0, 10)

            for _ in range(num_comments):
                Comment.objects.create(
                    post=post,
                    user=random.choice(users),
                    content=random.choice(sample_comments),
                    created_at=post.created_at
                    + timedelta(
                        hours=random.randint(
                            1, 24 * 7
                        ),  # Commentaire dans la semaine qui suit le post
                        minutes=random.randint(0, 59),
                    ),
                )
                comments_created += 1

            if num_comments > 0:
                self.stdout.write(
                    f"Créé {num_comments} commentaires pour le post {post.id}"
                )

        self.stdout.write(
            self.style.SUCCESS(f"{comments_created} commentaires créés avec succès !")
        )
