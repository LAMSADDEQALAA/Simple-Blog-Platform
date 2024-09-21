from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Seed users'

    def handle(self, *args, **kwargs):
                
        for i in range(10):
            user = User()
            user.username = f"user {i + 1}"
            user.set_password(f"user {i + 1}")
            user.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully created user: {user.username}'))

        self.stdout.write(self.style.SUCCESS('Seeding completed.'))