import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_blog.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Post

def create_posts():
    # Get users
    admin_user = User.objects.get(username='admin')
    user1 = User.objects.get(username='user1')
    user2 = User.objects.get(username='user2')
    
    # Get or create categories
    tech_category, tech_created = Category.objects.get_or_create(
        name='Technologie',
        defaults={'description': 'Articles sur les dernières innovations technologiques'}
    )
    if tech_created:
        print(f"Category created: {tech_category.name}")
    
    # Get other categories
    travel_category = Category.objects.get(name='Voyage')
    cooking_category = Category.objects.get(name='Cuisine')
    health_category = Category.objects.get(name='Santé')
    art_category = Category.objects.get(name='Art et Culture')
    
    # Create posts for admin
    admin_posts = [
        {
            'title': 'Bienvenue sur le blog personnel',
            'content': """Bienvenue sur notre nouvelle plateforme de blog personnel !

Ce site vous permet de partager vos pensées, expériences et opinions avec le monde entier. Que vous soyez passionné de technologie, de cuisine, de voyage ou d'art, vous trouverez ici un espace pour exprimer votre créativité.

N'hésitez pas à créer un compte, publier des articles et interagir avec les autres utilisateurs. Bonne exploration !""",
            'category': None
        },
        {
            'title': 'Les dernières avancées en IA',
            'content': """L'intelligence artificielle continue de progresser à pas de géant. Les modèles de langage comme GPT-4, Claude et Gemini repoussent les limites de ce que les machines peuvent comprendre et générer.

Ces avancées ont des implications profondes pour de nombreux secteurs, de la santé à l'éducation en passant par la créativité et les services financiers.

Que pensez-vous de ces développements ? Partagez vos réflexions dans les commentaires !""",
            'category': tech_category
        }
    ]
    
    # Create posts for user1
    user1_posts = [
        {
            'title': 'Mon voyage à Paris',
            'content': """J'ai récemment eu l'opportunité de visiter Paris, la ville lumière, et quelle expérience fabuleuse !

La Tour Eiffel, le Louvre, Notre-Dame (même en reconstruction), les Champs-Élysées... chaque coin de rue regorge d'histoire et de beauté.

Sans oublier la gastronomie française ! Les croissants frais du matin, les délicieux fromages et les pâtisseries exquises ont définitivement conquis mon cœur (et mon estomac).

Je vous recommande vivement cette destination si vous ne l'avez pas encore visitée.""",
            'category': travel_category
        },
        {
            'title': 'Recette de tarte aux pommes traditionnelle',
            'content': """Aujourd'hui, je partage avec vous ma recette familiale de tarte aux pommes.

Ingrédients :
- Pâte brisée
- 6 pommes Golden
- 50g de sucre
- 1 sachet de sucre vanillé
- Cannelle (optionnel)

Préparation :
1. Préchauffez le four à 180°C.
2. Étalez la pâte brisée dans un moule à tarte.
3. Épluchez et coupez les pommes en fines tranches.
4. Disposez les pommes sur la pâte.
5. Saupoudrez de sucre et de sucre vanillé.
6. Ajoutez un peu de cannelle si vous aimez.
7. Enfournez pour 30-35 minutes.

Servez tiède avec une boule de glace à la vanille. Bon appétit !""",
            'category': cooking_category
        }
    ]
    
    # Create posts for user2
    user2_posts = [
        {
            'title': 'Les bienfaits de la méditation quotidienne',
            'content': """Depuis que j'ai commencé à méditer tous les jours pendant 15 minutes, ma vie a radicalement changé.

La méditation m'a aidé à :
- Réduire mon stress et mon anxiété
- Améliorer ma concentration
- Mieux dormir
- Développer ma patience
- Augmenter ma créativité

Je recommande de commencer par de courtes sessions de 5 minutes et d'augmenter progressivement. Il existe d'excellentes applications comme Headspace ou Calm pour vous guider si vous êtes débutant.

Partagez vos expériences avec la méditation dans les commentaires !""",
            'category': health_category
        },
        {
            'title': 'Analyse du film "Parasite" de Bong Joon-ho',
            'content': """Le film "Parasite" du réalisateur sud-coréen Bong Joon-ho, Palme d'Or à Cannes et Oscar du meilleur film, est une œuvre magistrale qui mérite toute l'attention qu'elle a reçue.

Cette satire sociale brillante explore les inégalités de classes à travers l'histoire de deux familles - les Kim, qui vivent dans la pauvreté, et les Park, immensément riches.

Ce qui rend ce film si puissant est la façon dont il mélange les genres - comédie, thriller, drame - tout en maintenant une critique sociale acérée. La cinématographie est impeccable, notamment les contrastes visuels entre le sous-sol humide des Kim et la villa luxueuse des Park.

Sans spoiler l'intrigue, la fin vous laissera sans aucun doute avec beaucoup de réflexions sur notre société contemporaine.

Avez-vous vu ce film ? Qu'en avez-vous pensé ?""",
            'category': art_category
        }
    ]
    
    # Create posts for each user
    create_user_posts(admin_user, admin_posts)
    create_user_posts(user1, user1_posts)
    create_user_posts(user2, user2_posts)

def create_user_posts(user, posts_data):
    for post_data in posts_data:
        # Check if post with this title and author already exists
        if not Post.objects.filter(title=post_data['title'], author=user).exists():
            post = Post.objects.create(
                title=post_data['title'],
                content=post_data['content'],
                author=user,
                category=post_data['category'],
                date_posted=timezone.now()
            )
            print(f"Post created: '{post.title}' by {user.username}")
        else:
            print(f"Post '{post_data['title']}' by {user.username} already exists")

if __name__ == '__main__':
    print("Creating sample blog posts...")
    create_posts()
    print("\nSample posts created successfully!") 