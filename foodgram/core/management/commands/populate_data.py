from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Seller, Post, Like
from faker import Faker
import random
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Populates the database with initial data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Step 1: Create Users and Sellers
        users = []
        sellers = []
        food_related_bios = [
            "A passionate chef with a love for creating unique and delicious meals. Specializes in Italian cuisine and fresh, organic ingredients.",
            "Food blogger and culinary artist dedicated to bringing the joy of cooking to everyone's kitchen. Expert in quick and easy weeknight dinners.",
            "Seasoned baker with a knack for making mouth-watering desserts. From cakes to cookies, every sweet treat is made with love.",
            "Home cook turned professional chef, focused on healthy and nutritious meals that don't compromise on flavor. Specializes in vegetarian dishes.",
            "A culinary explorer who loves to experiment with new flavors and techniques. Known for crafting gourmet dishes with a creative twist."
        ]

        for i in range(5):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}.{last_name.lower()}"
            email = f"{first_name.lower()}.{last_name.lower()}@example.com"

            user = User.objects.create_user(
                username=username,
                password='password123',
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            users.append(user)

            # Create a Seller profile for each user with a food-related bio
            seller = Seller.objects.create(
                user=user,
                bio=food_related_bios[i % len(food_related_bios)]  # Rotate through the food-related bios
            )
            sellers.append(seller)

        # Step 2: Define the local images
        food_images = [
            os.path.join('food_images', 'pizza.jpg'),
            os.path.join('food_images', 'burger.jpg'),
            os.path.join('food_images', 'soup.jpg'),
            os.path.join('food_images', 'spaghetti.jpg'),
            os.path.join('food_images', 'salad.jpg'),
        ]

        food_descriptions = [
            "Delicious homemade pizza with fresh ingredients",
            "Juicy grilled burger with cheese and bacon",
            "Hearty bowl of chicken noodle soup",
            "Spaghetti carbonara with creamy sauce",
            "Fresh Caesar salad with crispy croutons",
        ]

        # Step 3: Create Posts for each Seller
        posts = []
        for seller in sellers:
            for i in range(5):
                post = Post.objects.create(
                    seller=seller,
                    image=food_images[i % len(food_images)],  # Rotate through the images
                    description=food_descriptions[i % len(food_descriptions)],
                    price=random.uniform(5.0, 25.0)
                )
                posts.append(post)

        # Step 4: Create Likes for Posts
        for user in users:
            liked_posts = random.sample(posts, k=3)  # Each user likes 3 random posts
            for post in liked_posts:
                Like.objects.create(user=user, post=post)

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
