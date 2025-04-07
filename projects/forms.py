# from django import forms
# from .models import Project, ProjectImage, Tag
# from django.forms import modelformset_factory
# from django import forms
# from .models import Project, ProjectImage, Donation , Comment, Rating
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _
# from django.utils import timezone
# from django.core.files.images import get_image_dimensions
# from django.core.files import File

# class ProjectForm(forms.ModelForm):
#     tags = forms.ModelMultipleChoiceField(
#         queryset=Tag.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False,  # Make tags optional
#         help_text="Select tags (optional)"
#     )

#     class Meta:
#         model = Project
#         fields = ['title', 'details', 'total_target', 'tags', 'start_time', 'end_time']
    
# class ProjectImageForm(forms.ModelForm):
#     class Meta:
#         model = ProjectImage
#         fields = ['image']

# # Optional: Allow multiple image uploads for the project
# ProjectImageFormSet = modelformset_factory(ProjectImage, form=ProjectImageForm, extra=3)

# ########################################################################################################

# class DonationForm(forms.ModelForm):
#     class Meta:
#         model = Donation
#         fields = ['amount']
# ############################################################################################################

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['text']
# #############################################################################################################

# class RatingForm(forms.ModelForm):
#     class Meta:
#         model = Rating
#         fields = ['score']

# ############################################################################################################



from django import forms
from .models import Project, ProjectImage, Tag, Donation, Comment, Rating
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.files.images import get_image_dimensions
from django.core.files import File

class ProjectForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,  # Make tags optional
        help_text="Select tags (optional)",
    )

    class Meta:
        model = Project
        fields = ['title', 'details', 'total_target', 'tags', 'start_time', 'end_time']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project title'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter project details'}),
            'total_target': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter target amount'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

# Optional: Allow multiple image uploads for the project
ProjectImageFormSet = modelformset_factory(ProjectImage, form=ProjectImageForm, extra=3)

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter donation amount'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Leave a comment'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5, 'placeholder': 'Rate from 1 to 5'}),
        }
