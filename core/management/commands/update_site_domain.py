from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Set the django Site domain from APP_DOMAIN or provided --domain.'

    def add_arguments(self, parser):
        parser.add_argument('--domain', type=str, help='Domain to set (overrides APP_DOMAIN)')

    def handle(self, *args, **options):
        domain = options.get('domain') or getattr(settings, 'APP_DOMAIN', None)
        if not domain:
            self.stderr.write('No domain provided and APP_DOMAIN not set.')
            return

        try:
            from django.contrib.sites.models import Site

            site, created = Site.objects.get_or_create(pk=1, defaults={'domain': domain, 'name': domain})
            site.domain = domain
            site.name = domain
            site.save()
            self.stdout.write(self.style.SUCCESS(f'Site domain set to: {domain}'))
        except Exception as exc:
            self.stderr.write(f'Failed to update Site.domain: {exc}')
