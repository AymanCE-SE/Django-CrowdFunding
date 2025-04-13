from django import forms
from django.forms import inlineformset_factory
from .models import Project, ProjectImage, Tag, Donation, Comment, Rating, Category, Report
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
    
    tags_input = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Project
        fields = ['title', 'category', 'details', 'total_target', 'start_time', 'end_time']
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
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Leave a comment', 'rows': 2}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5, 'placeholder': 'Rate from 1 to 5'}),
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason']
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-select'})
        }
