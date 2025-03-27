import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_blog.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post, Comment

def create_comments():
    # Get users
    admin_user = User.objects.get(username='admin')
    user1 = User.objects.get(username='user1')
    user2 = User.objects.get(username='user2')
    
    # Get all posts
    posts = Post.objects.all()
    
    # Comments data with user
    comment_data = [
        # Admin comments on user posts
        {
            'post_title': 'Mon voyage à Paris',
            'author': admin_user,
            'content': "Paris est vraiment magnifique ! J'ai adoré visiter le musée d'Orsay lors de mon dernier voyage."
        },
        {
            'post_title': 'Les bienfaits de la méditation quotidienne',
            'author': admin_user,
            'content': "Excellent article ! J'ai commencé à méditer il y a 6 mois et les bénéfices sont réels. Je recommande l'application Insight Timer pour les débutants."
        },
        # User1 comments on admin and user2 posts
        {
            'post_title': 'Les dernières avancées en IA',
            'author': user1,
            'content': "C'est fascinant et un peu effrayant en même temps ! Je me demande comment cela va transformer le marché du travail dans les prochaines années."
        },
        {
            'post_title': 'Analyse du film "Parasite" de Bong Joon-ho',
            'author': user1,
            'content': "J'ai adoré ce film ! La façon dont il mélange les genres est vraiment unique et la critique sociale est à la fois subtile et percutante."
        },
        # User2 comments on admin and user1 posts
        {
            'post_title': 'Bienvenue sur le blog personnel',
            'author': user2,
            'content': "Merci pour cette plateforme ! Je suis ravi de pouvoir partager mes expériences ici."
        },
        {
            'post_title': 'Recette de tarte aux pommes traditionnelle',
            'author': user2,
            'content': "J'ai essayé cette recette hier et c'était délicieux ! J'ai ajouté un peu de caramel et c'était parfait."
        }
    ]
    
    # Anonymous comments
    anonymous_comments = [
        {
            'post_title': 'Bienvenue sur le blog personnel',
            'author_name': 'Visiteur Curieux',
            'content': "Je viens de découvrir ce blog et je suis impressionné par la qualité des articles. Je reviendrai !"
        },
        {
            'post_title': 'Les dernières avancées en IA',
            'author_name': 'Techno Enthousiaste',
            'content': "Article très instructif ! Est-ce que vous prévoyez d'aborder la question de la régulation de l'IA dans un prochain post ?"
        }
    ]
    
    # Create user comments
    for comment in comment_data:
        post = Post.objects.get(title=comment['post_title'])
        if not Comment.objects.filter(
            post=post, 
            author=comment['author'], 
            content=comment['content']
        ).exists():
            Comment.objects.create(
                post=post,
                author=comment['author'],
                content=comment['content'],
                date_posted=timezone.now()
            )
            print(f"Comment by {comment['author'].username} added to post '{post.title}'")
        else:
            print(f"Comment by {comment['author'].username} on post '{post.title}' already exists")
    
    # Create anonymous comments
    for comment in anonymous_comments:
        post = Post.objects.get(title=comment['post_title'])
        if not Comment.objects.filter(
            post=post, 
            author_name=comment['author_name'], 
            content=comment['content']
        ).exists():
            Comment.objects.create(
                post=post,
                author_name=comment['author_name'],
                content=comment['content'],
                date_posted=timezone.now()
            )
            print(f"Anonymous comment by {comment['author_name']} added to post '{post.title}'")
        else:
            print(f"Anonymous comment by {comment['author_name']} on post '{post.title}' already exists")

if __name__ == '__main__':
    print("Creating sample comments...")
    create_comments()
    print("\nSample comments created successfully!") 