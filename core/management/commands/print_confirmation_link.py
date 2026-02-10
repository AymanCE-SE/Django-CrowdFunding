from django.core.management.base import BaseCommand
from django.conf import settings
from django.urls import reverse


class Command(BaseCommand):
    help = 'Generate and print an allauth email confirmation URL for a given user email.'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='User email to generate confirmation for')
        parser.add_argument('--domain', type=str, help='Domain to use (overrides APP_DOMAIN or Site.domain)')
        parser.add_argument('--protocol', type=str, choices=['http', 'https'], help='Protocol to use in URL')

    def handle(self, *args, **options):
        email = options.get('email')
        domain = options.get('domain') or getattr(settings, 'APP_DOMAIN', None)
        protocol = options.get('protocol')

        # Determine default protocol
        if not protocol:
            protocol = 'https' if not getattr(settings, 'DEBUG', True) else 'http'

        try:
            from django.contrib.auth import get_user_model
            from allauth.account.models import EmailAddress, EmailConfirmation
            from django.contrib.sites.models import Site

            User = get_user_model()
            user = User.objects.filter(email__iexact=email).first()
            if not user:
                self.stderr.write(f'No user found with email: {email}')
                return

            email_address, created = EmailAddress.objects.get_or_create(
                user=user, email=email, defaults={'verified': False, 'primary': False}
            )

            confirmation = EmailConfirmation.create(email_address)
            url_path = reverse('account_confirm_email', args=[confirmation.key])

            if not domain:
                try:
                    domain = Site.objects.get_current().domain
                except Exception:
                    domain = 'localhost'

            full_url = f"{protocol}://{domain}{url_path}"
            self.stdout.write(full_url)

        except Exception as exc:
            self.stderr.write(f'Error generating confirmation link: {exc}')
