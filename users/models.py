from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Sum, Count
from decimal import Decimal

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

    def get_my_projects(self):
        """Get all projects created by the user"""
        return self.created_projects.all().annotate(
            donation_count=Count('donations'),
            comment_count=Count('comments')
        )

    def get_active_projects(self):
        """Get user's active projects"""
        return self.created_projects.filter(
            end_time__gt=timezone.now()
        ).order_by('end_time')

    def get_completed_projects(self):
        """Get user's completed projects"""
        return self.created_projects.filter(
            end_time__lte=timezone.now()
        ).order_by('-end_time')

    def get_my_donations(self):
        """Get all donations made by the user"""
        return self.donation_set.select_related('project').order_by('-created_at')

    def get_total_donated(self):
        """Get total amount donated by the user"""
        total = self.donation_set.aggregate(
            total=Sum('amount')
        )['total']
        return total if total else Decimal('0.00')

    def get_recent_activities(self, limit=5):
        """Get user's recent activities (donations, comments, ratings)"""
        donations = self.donation_set.all()
        comments = self.comment_set.all()
        ratings = self.rating_set.all()
        
        activities = []
        
        for donation in donations:
            activities.append({
                'type': 'donation',
                'date': donation.created_at,
                'project': donation.project,
                'amount': donation.amount
            })
            
        for comment in comments:
            activities.append({
                'type': 'comment',
                'date': comment.created_at,
                'project': comment.project,
                'text': comment.text
            })
            
        for rating in ratings:
            activities.append({
                'type': 'rating',
                'date': rating.created_at,
                'project': rating.project,
                'score': rating.score
            })
        
        return sorted(
            activities, 
            key=lambda x: x['date'], 
            reverse=True
        )[:limit]

    def get_donation_stats(self):
        """Get donation statistics"""
        return {
            'total_donated': self.get_total_donated(),
            'projects_supported': self.donation_set.values('project').distinct().count(),
            'total_donations': self.donation_set.count(),
            'average_donation': self.donation_set.aggregate(
                avg=models.Avg('amount')
            )['avg'] or 0
        }

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