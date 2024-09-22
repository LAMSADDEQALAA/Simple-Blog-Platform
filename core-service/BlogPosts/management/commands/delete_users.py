from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'deleting  blog posts'

    def handle(self, *args, **kwargs):

        User.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('BlogPost deletion completed.'))