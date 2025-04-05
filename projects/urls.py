from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='project_list'),  
    path('create/', views.create_project, name='create_project'),
    path('<int:pk>/donate/', views.donate_to_project, name='donate_to_project'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/rate/', views.rate_project, name='rate_project'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
]