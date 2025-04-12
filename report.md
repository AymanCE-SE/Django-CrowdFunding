<!-- @format -->

# Crowd-Funding Project Report

## 1. Project Overview

The Crowd-Funding Project is a Django-based web application that allows users to create, manage, and support projects. It includes features such as:

- Project creation, editing, and deletion
- Donation functionality
- User authentication and profile management
- Project rating and commenting
- Category and tag-based filtering
- AJAX-based search and filtering
- Testimonials and top donor sections

---

## 2. Project Description Logic

### 2.1. Project Model

The `Project` model in `projects/models.py` defines the core attributes of a project:

```python
class Project(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField()  # Full project description
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    donated_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_projects')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    tags = models.ManyToManyField('Tag', related_name='projects', blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
```
