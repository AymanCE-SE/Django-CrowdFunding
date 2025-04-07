from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import CustomUser, Profile

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',  
            'first_name',
            'last_name', 
            'email',
            'phone_number',
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
        fields = ['profile_picture', 'birth_date', 'facebook_profile', 'country']
        widgets = {
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'facebook_profile': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://facebook.com/your.profile'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your country'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'd-none',
                'accept': 'image/*'
            })
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ' ',  # Empty placeholder for floating label
            'id': 'floatingUsername',
            'autocomplete': 'username',
            'autofocus': True
        }),
        error_messages={
            'required': 'Please enter your username'
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ' ',  # Empty placeholder for floating label
            'id': 'floatingPassword',
            'autocomplete': 'current-password'
        }),
        error_messages={
            'required': 'Please enter your password'
        }
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.error_messages['invalid_login'] = 'Invalid username or password. Please try again.'

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is not registered.")
        return email

