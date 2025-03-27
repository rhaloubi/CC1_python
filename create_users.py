import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_blog.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category

def create_users():
    # Create admin user
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        print(f"Admin user created: {admin_user.username}")
    else:
        print("Admin user already exists")
    
    # Create regular users
    if not User.objects.filter(username='user1').exists():
        user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='userpass123'
        )
        print(f"Regular user created: {user1.username}")
    else:
        print("User1 already exists")
    
    if not User.objects.filter(username='user2').exists():
        user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='userpass123'
        )
        print(f"Regular user created: {user2.username}")
    else:
        print("User2 already exists")

def create_categories():
    # Create some basic categories
    categories = [
        {'name': 'Technologie', 'description': 'Articles sur les dernières innovations technologiques'},
        {'name': 'Voyage', 'description': 'Partage d\'expériences de voyage et conseils'},
        {'name': 'Cuisine', 'description': 'Recettes et astuces culinaires'},
        {'name': 'Santé', 'description': 'Conseils pour une vie saine'},
        {'name': 'Art et Culture', 'description': 'Discussions sur l\'art, la littérature et la culture'}
    ]
    
    for category_data in categories:
        if not Category.objects.filter(name=category_data['name']).exists():
            category = Category.objects.create(
                name=category_data['name'],
                description=category_data['description']
            )
            print(f"Category created: {category.name}")
        else:
            print(f"Category '{category_data['name']}' already exists")

if __name__ == '__main__':
    print("Creating users...")
    create_users()
    print("\nCreating categories...")
    create_categories()
    print("\nSetup completed!") 