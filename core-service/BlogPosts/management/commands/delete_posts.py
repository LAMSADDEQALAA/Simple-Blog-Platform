from django.core.management.base import BaseCommand
from BlogPosts.models import BlogPost
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'deleting  blog posts'

    def handle(self, *args, **kwargs):

        BlogPost.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('BlogPost deletion completed.'))