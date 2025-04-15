from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from users.views import CustomLoginView  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('projects.urls')),
    path('accounts/', include('allauth.urls')),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
