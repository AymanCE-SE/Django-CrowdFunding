from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list'),  
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:pk>/donate/', views.donate_to_project, name='donate_to_project'),
    path('projects/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('projects/<int:pk>/rate/', views.rate_project, name='rate_project'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/edit/<int:pk>/', views.edit_project, name='edit_project'),
    path('projects/delete/<int:pk>/', views.delete_project, name='delete_project'),
    path('projects/<int:project_id>/submit_report/', views.submit_report, name='submit_report'),
]