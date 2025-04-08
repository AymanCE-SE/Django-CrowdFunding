from django import forms
from django.forms import inlineformset_factory
from .models import Project, ProjectImage, Tag, Donation, Comment, Rating, Category
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ProjectForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )
    
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False
    )

    class Meta:
        model = Project
        fields = ['title', 'category', 'details', 'total_target', 'tags', 'start_time', 'end_time']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project title'
            }),
            'details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your project'
            }),
            'total_target': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter target amount'
            }),
            'start_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise ValidationError({
                'end_time': _('End time must be after start time')
            })
        return cleaned_data

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

# Use inlineformset_factory to tie ProjectImages to a specific Project
# - extra=1 ensures one blank form is rendered (so there’s always at least one)
# - max_num=5 and validate_max=True restrict the total images to five
# - can_delete=True allows removing an image if needed
ProjectImageFormSet = inlineformset_factory(
    Project, 
    ProjectImage, 
    form=ProjectImageForm, 
    extra=1, 
    can_delete=True,
    max_num=5,
    validate_max=True,
    fields=('image',)
)

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
