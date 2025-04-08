from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import ProgrammingError
from projects.models import Category, Tag

class Command(BaseCommand):
    help = 'Creates default categories'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                # Create categories
                categories = [
                    'Education',
                    'Health & Wellness',
                    'Technology',
                    'Arts & Creative',
                    'Community',
                    'Business'
                ]
                
                for name in categories:
                    Category.objects.get_or_create(
                        name=name,
                        defaults={'name': name}
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Category "{name}" created')
                    )

                # Create tags
                tags = [
                    'Innovation',
                    'Research',
                    'Startup',
                    'Social Impact',
                    'Healthcare',
                    'Education',
                ]
                
                for name in tags:
                    Tag.objects.get_or_create(
                        name=name,
                        defaults={'name': name}
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Tag "{name}" ensured')
                    )

        except ProgrammingError as e:
            self.stdout.write(
                self.style.ERROR(f'Database error: {str(e)}. Run migrations first.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Unexpected error: {str(e)}')
            )