from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('skills/', views.SkillsView.as_view(), name='skills'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # API endpoints
    path('api/projects/', views.api_projects, name='api_projects'),
    path('api/skills/', views.api_skills, name='api_skills'),
    

]
