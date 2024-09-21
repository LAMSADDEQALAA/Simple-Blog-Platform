from django.core.management.base import BaseCommand
from BlogPosts.models import BlogPost
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Seed blog posts'

    def handle(self, *args, **kwargs):
        if not User.objects.exists():
            self.stdout.write(self.style.WARNING('No users found. Please create a user first.'))
            return
        
        users = User.objects.all()
        
        for i in range(50):
            title = f'Blog Post {i + 1}'
            content = f'This is the content for blog post {i + 1}.'
            author = random.choice(users)
            
            BlogPost.objects.create(title=title, content=content, author=author)
            self.stdout.write(self.style.SUCCESS(f'Successfully created blog post: {title}'))

        self.stdout.write(self.style.SUCCESS('Seeding completed.'))