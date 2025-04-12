from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import timedelta
from django.utils.timezone import now


class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{user.password}{timestamp}"

    def check_token(self, user, token):
        # Call the parent method to validate the token structure
        if not super().check_token(user, token):
            return False

        # Check if the token is expired (24 days)
        timestamp = self._get_timestamp(token)
        token_age = now() - timedelta(seconds=timestamp * 60)
        return token_age.days <= 24
