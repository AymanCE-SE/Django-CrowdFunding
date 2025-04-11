from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
        db_table = 'projects_category'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'projects_tag'


class Project(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField()
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_projects'  # Add this for easier access to user's projects
    )
    category = models.ForeignKey(
        'Category', 
        on_delete=models.SET_NULL,
        null=True,
        blank=True, 
        related_name='projects'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    average_rating = models.FloatField(default=0, blank=True)
    tags = models.ManyToManyField(Tag)
    donated_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_by']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self) -> str:
        return self.title

    @property
    def progress(self):
        """Calculate funding progress as a percentage"""
        if self.total_target == 0:
            return 0
        return int((self.donated_amount / self.total_target) * 100)

    @property
    def is_active(self):
        """Check if project is currently active for donations"""
        now = timezone.now()
        return (self.start_time <= now <= self.end_time and 
                self.donated_amount < self.total_target)

    @property
    def time_remaining(self):
        """Calculate time remaining for the project"""
        if self.end_time < timezone.now():
            return "Expired"
        delta = self.end_time - timezone.now()
        days = delta.days
        if days > 0:
            return f"{days} days left"
        hours = delta.seconds // 3600
        return f"{hours} hours left"

    def add_donation(self, user, amount):
        """Add a donation and update the donated amount"""
        if not self.is_active:
            raise ValueError("This project is not active")
        
        donation = Donation.objects.create(
            user=user,
            project=self,
            amount=amount
        )
        self.donated_amount += Decimal(amount)
        self.save()
        return donation

    def get_user_donation(self, user):
        """Get total donation amount for a specific user"""
        return self.donations.filter(user=user).aggregate(
            total=models.Sum('amount')
        )['total'] or 0

    def get_top_donors(self, limit=5):
        """Get top donors for the project"""
        return self.donations.values(
            'user__username', 'user__id'
        ).annotate(
            total_amount=models.Sum('amount')
        ).order_by('-total_amount')[:limit]

    def get_donation_stats(self):
        """Get project donation statistics"""
        return {
            'total_donors': self.donations.values('user').distinct().count(),
            'total_donations': self.donations.count(),
            'average_donation': self.donations.aggregate(
                avg=models.Avg('amount')
            )['avg'] or 0,
            'progress_percentage': self.progress
        }

    def get_activity_summary(self):
        """Get project activity summary"""
        return {
            'total_comments': self.comments.count(),
            'total_ratings': self.ratings.count(),
            'average_rating': self.ratings.aggregate(
                avg=models.Avg('score')
            )['avg'] or 0
        }

    def is_donated_by(self, user):
        """Check if user has donated to this project"""
        return self.donations.filter(user=user).exists()

    def get_similar_projects(self, limit=3):
        """Get similar projects based on tags"""
        return Project.objects.filter(
            tags__in=self.tags.all()
        ).exclude(
            id=self.id
        ).distinct()[:limit]

    def get_first_image(self):
        first_image = self.images.first()  # Using the related_name
        if first_image:
            return first_image.image.url
        return None

    def get_status(self):
        """Get the current status of the project"""
        now = timezone.now()
        if self.donated_amount >= self.total_target:
            return 'funded'
        elif now < self.start_time:
            return 'coming_soon'
        elif now > self.end_time:
            return 'ended'
        else:
            return 'active'

    def get_status_message(self):
        """Get a user-friendly status message"""
        status = self.get_status()
        now = timezone.now()
        
        messages = {
            'funded': 'Project has been fully funded!',
            'coming_soon': f'Project starts in {(self.start_time - now).days} days',
            'ended': 'Project has ended',
            'active': f'Still needs {self.total_target - self.donated_amount:.2f} EGP'
        }
        return messages[status]

    def can_be_deleted(self):
        """Check if project can be deleted based on donation percentage"""
        if self.total_target == 0:
            return True
        donation_percentage = (self.donated_amount / self.total_target) * 100
        return donation_percentage < 25

    def get_donation_percentage(self):
        """Get the percentage of donations received"""
        if self.total_target == 0:
            return 0
        return (self.donated_amount / self.total_target) * 100

    def is_owner(self, user):
        """Check if user is the project owner"""
        return self.created_by == user

    def calculate_average_rating(self):
        """Calculate and return the average rating"""
        avg = self.ratings.aggregate(Avg('score'))['score__avg'] or 0
        return round(avg, 2)

    def update_average_rating(self):
        """Update the stored average rating"""
        self.average_rating = self.calculate_average_rating()
        self.save(update_fields=['average_rating'])

    def get_related_projects(self):
        """Get related projects based on category and tags"""
        return Project.objects.filter(
            models.Q(category=self.category) | 
            models.Q(tags__in=self.tags.all())
        ).exclude(
            id=self.id
        ).distinct().order_by(
            '-created_at'
        )[:5]


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE,
        related_name='images'  # Add this related_name
    )
    image = models.ImageField(upload_to='projects/')
    
    def __str__(self):
        return f"Image for {self.project.title}"

############################################################################
class Donation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='donations', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} donated {self.amount} to {self.project}"
###################################################################################################

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        if self.parent:
            return f"Reply by {self.user} to {self.parent.user} on {self.project}"
        return f"Comment by {self.user} on {self.project}"

##########################################################################################################

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='ratings', on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 scale
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating by {self.user} on {self.project}"


class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('project', 'Project'),
        ('comment', 'Comment'),
    ]

    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate Content'),
        ('harassment', 'Harassment'),
        ('fraud', 'Fraud'),
        ('copyright', 'Copyright Violation'),
        ('offensive', 'Offensive Content'),
        ('hate_speech', 'Hate Speech'),
        ('false_information', 'False Information'),
        ('other', 'Other'),
    ]

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_type} report by {self.reporter}"