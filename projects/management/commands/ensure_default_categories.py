from django.core.management.base import BaseCommand
from projects.models import Category

class Command(BaseCommand):
    help = 'Ensures default categories exist'

    def handle(self, *args, **kwargs):
        default_categories = [
            'Technology',
            'Art & Design',
            'Community Projects'
        ]

        for category_name in default_categories:
            Category.objects.get_or_create(name=category_name)
        
        self.stdout.write(self.style.SUCCESS('Default categories created successfully'))