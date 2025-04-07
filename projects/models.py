from django.db import models
from django.conf import settings


# class Category(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self) -> str:
#         return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField()
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    tags = models.ManyToManyField(Tag)
    donated_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_images/')

    def __str__(self) -> str:
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

    def __str__(self):
        return f"Comment by {self.user} on {self.project}"
##########################################################################################################

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='ratings', on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 scale
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating by {self.user} on {self.project}"


###############################################################################################################
