from django import forms
from .models import Project, ProjectImage, Tag
from django.forms import modelformset_factory
from django import forms
from .models import Project, ProjectImage, Donation , Comment, Rating
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.files.images import get_image_dimensions
from django.core.files import File

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'total_target', 'tags', 'start_time', 'end_time']

    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)
    
class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image']

# Optional: Allow multiple image uploads for the project
ProjectImageFormSet = modelformset_factory(ProjectImage, form=ProjectImageForm, extra=3)

########################################################################################################

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount']
############################################################################################################

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
#############################################################################################################

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']

############################################################################################################
