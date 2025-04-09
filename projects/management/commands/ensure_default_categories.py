from django.core.management.base import BaseCommand
from django.db import transaction
from projects.models import Category

class Command(BaseCommand):
    help = 'Creates default categories'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                categories = [
                    'Education',
                    'Health & Wellness',
                    'Technology',
                    'Arts & Creative',
                    'Community',
                    'Business',
                    'Environment',
                    'Sports',
                    'Travel',
                ]
                
                for name in categories:
                    category, created = Category.objects.get_or_create(name=name)
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f'Category "{name}" created')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'Category already exists: {name}')
                        )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )