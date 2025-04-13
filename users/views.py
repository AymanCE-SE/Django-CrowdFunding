from .forms import UserRegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate
from django.contrib import messages
from .forms import ProfileUpdateForm
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.views import PasswordResetView
from .utils import CustomPasswordResetTokenGenerator
from django.contrib.auth.views import PasswordResetConfirmView

User = get_user_model()


class CustomPasswordResetView(PasswordResetView):
    # token_generator = CustomPasswordResetTokenGenerator()
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = '/password-reset/done/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)  # Debugging: Print the context to the console
        return context


# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     token_generator = CustomPasswordResetTokenGenerator()
#     success_url = '/password-reset-complete/'


@login_required
def profile_view(request):
    user = request.user
    context = {
        "active_projects": user.get_active_projects(),
        "completed_projects": user.get_completed_projects(),
        "recent_donations": user.get_my_donations()[:5],
        "donation_stats": user.get_donation_stats(),
    }
    return render(request, "profile/profile.html", context)


@login_required
def profile_edit(request):
    """Edit user profile"""
    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("users:profile")
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, "profile/profile_edit.html", {"form": form})


@login_required
def delete_account(request):
    """Delete user account"""
    if request.method == "POST":
        password = request.POST.get("password")
        user = authenticate(username=request.user.username, password=password)

        if user is not None:
            user.delete()
            messages.success(request, "Your account has been deleted.")
            return redirect("users:profile")  # Update this line
        else:
            messages.error(request, "Password is incorrect. Account not deleted.")

    return render(request, "profile/delete_account.html")


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until confirmed
            user.save()

            # Use request.get_host() for the domain
            domain = request.get_host()

            # Create the activation URL manually
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = f"http://{domain}{reverse('users:activate', kwargs={'uid': uid, 'token': token})}"

            subject = "Activate your Crowdfunding account"
            message = render_to_string(
                "registration/account_activation_email.html",
                {
                    "user": user,
                    "activation_link": activation_link,  # Pass the URL directly
                },
            )

            user.email_user(subject, message)

            messages.success(
                request, 'Account created successfully! You can now log in.'
            )
            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, "registration/register.html", {"form": form})


def activate(request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))  # Updated here
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, "Your account has been activated! You can now log in."
        )
        return redirect("login")
    else:
        return render(request, "registration/activation_invalid.html")

