from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, update_session_auth_hash, authenticate
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
from .forms import ProfileUpdateForm, UserRegisterForm
from django.urls import reverse

User = get_user_model()

@login_required
def profile_view(request):
    """View user's profile"""
    profile = Profile.objects.first()
    
    context = {
        'profile': profile,
        'projects': [],  # Add empty list for now
        'donations': []  # Add empty list for now
    }
    return render(request, 'profile/profile.html', context)

@login_required
def profile_edit(request):
    """Edit user profile"""
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:profile')  # Update this line
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'profile_form': profile_form,
    }
    return render(request, 'profile/profile_edit.html', context)

@login_required
def delete_account(request):
    """Delete user account"""
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        
        if user is not None:
            user.delete()
            messages.success(request, 'Your account has been deleted.')
            return redirect('users:profile')  # Update this line
        else:
            messages.error(request, 'Password is incorrect. Account not deleted.')
    
    return render(request, 'profile/delete_account.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})