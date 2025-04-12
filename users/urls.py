from django.urls import path, reverse_lazy, include
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomPasswordResetForm

app_name = "users"

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/delete/', views.delete_account, name='delete_account'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt',
             success_url=reverse_lazy('users:password_reset_done'),
             form_class=CustomPasswordResetForm
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url=reverse_lazy(
                 'users:password_reset_complete')  # Correct namespace
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='registration/logout.html',
        next_page='/',
    ), name='logout'),
    # path('accounts/', include('allauth.urls')),
]
