from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Update the django Site object domain from environment variable so
        # allauth and other email builders use the correct domain for links.
        try:
            from django.contrib.sites.models import Site
            from django.db import OperationalError, ProgrammingError

            domain = getattr(settings, 'APP_DOMAIN', None)
            if domain:
                try:
                    site = Site.objects.get_current()
                    if site.domain != domain:
                        site.domain = domain
                        site.name = domain
                        site.save()
                except (OperationalError, ProgrammingError):
                    # Database isn't ready (migrations not applied) — skip.
                    pass
        except Exception:
            # Defensive: don't break startup if something goes wrong here
            pass
