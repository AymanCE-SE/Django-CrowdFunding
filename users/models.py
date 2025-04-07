from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^01[0125][0-9]{8}$',
        message="Phone number must be an Egyptian number. Format: '01xxxxxxxxx'"
    )

    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=11,
        unique=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number']

    def clean(self):
        if not self.first_name or not self.last_name:
            raise ValidationError('First name and last name are required.')

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    profile_picture = models.ImageField(  # Moved from CustomUser to Profile
        upload_to='profile_pics/',
        null=True,
        blank=True
    )
    birth_date = models.DateField(null=True, blank=True)
    facebook_profile = models.URLField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"

# Signal to create profile when user is created
@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()