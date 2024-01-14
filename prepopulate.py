import os
import random
import string
from faker import Faker
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rating.settings')
application = get_wsgi_application()

from social.models import Post, UserRating
from django.contrib.auth.models import User

fake = Faker()


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


def generate_random_users(n=10):
    users_list = []
    for _ in range(n):
        username = fake.user_name()
        password = generate_random_password()
        user = User.objects.create(username=username, password=password)
        users_list.append(user.id)
    return users_list


def generate_random_posts(users_list, n=10):
    posts_list = []
    for _ in range(n):
        title = fake.sentence()
        content = fake.paragraph()
        post = Post.objects.create(title=title, content=content, author_id=random.choice(users_list))
        posts_list.append(post.id)
    return posts_list


def generate_random_ratings(users_list, posts_list, n=40):
    for _ in range(n):
        try:
            UserRating.objects.create(user_id=random.choice(users_list), post_id=random.choice(posts_list),
                                      rate=random.randint(1, 10))
        except Exception as e:
            pass


if __name__ == "__main__":
    users = generate_random_users()
    posts = generate_random_posts(users)
    generate_random_ratings(users, posts)
