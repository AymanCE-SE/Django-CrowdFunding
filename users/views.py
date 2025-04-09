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
    user = request.user
    context = {
        'active_projects': user.get_active_projects(),
        'completed_projects': user.get_completed_projects(),
        'recent_donations': user.get_my_donations()[:5],
        'donation_stats': user.get_donation_stats(),
    }
    return render(request, 'profile/profile.html', context)

@login_required
def profile_edit(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'profile/profile_edit.html', {'form': form})

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
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Profile is automatically created via signals
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# @PermissionRequiredMixin>>admin
