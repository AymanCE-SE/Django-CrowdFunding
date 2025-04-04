from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Profile

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',  
            'first_name',
            'last_name', 
            'email',
            'phone_number',
            'profile_picture',
            'password1',
            'password2'
        )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('first_name') or not cleaned_data.get('last_name'):
            raise ValidationError('First name and last name are required')
        return cleaned_data

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birth_date', 'facebook_profile', 'country']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }