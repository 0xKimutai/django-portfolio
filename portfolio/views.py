from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import Project, Skill, ContactMessage, Experience, Certification, Education
from .forms import ContactForm, ProjectFilterForm

class HomeView(TemplateView):
    """Enhanced home view with cached data"""
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Cache key for home page data
        cache_key = 'home_page_data'
        cached_data = cache.get(cache_key)
        
        if cached_data is None:
            # Fetch featured projects and skills
            featured_projects = Project.objects.filter(
                is_featured=True, 
                status='completed'
            ).order_by('-order', '-created_at')[:6]
            
            featured_skills = Skill.objects.filter(
                is_featured=True
            ).order_by('category', '-proficiency')[:12]
            
            current_experience = Experience.objects.filter(
                is_current=True
            ).first()
            
            recent_certifications = Certification.objects.filter(
                is_active=True
            ).order_by('-issue_date')[:3]
            
            cached_data = {
                'featured_projects': featured_projects,
                'featured_skills': featured_skills,
                'current_experience': current_experience,
                'recent_certifications': recent_certifications,
            }
            
            # Cache for 1 hour
            cache.set(cache_key, cached_data, 3600)
        
        context.update(cached_data)
        return context

class AboutView(TemplateView):
    """Enhanced about view with comprehensive data"""
    template_name = 'about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all experience, education, and skills
        experiences = Experience.objects.all().order_by('-start_date')
        education = Education.objects.all().order_by('-end_date', '-start_date')
        skills_by_category = {}
        
        for skill in Skill.objects.all():
            category = skill.get_category_display()
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(skill)
        
        context.update({
            'experiences': experiences,
            'education': education,
            'skills_by_category': skills_by_category,
        })
        return context

class ProjectListView(ListView):
    """Enhanced project list view with filtering and pagination"""
    model = Project
    template_name = 'projects.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Project.objects.all()
        
        # Apply filters
        form = ProjectFilterForm(self.request.GET)
        if form.is_valid():
            project_type = form.cleaned_data.get('project_type')
            status = form.cleaned_data.get('status')
            featured_only = form.cleaned_data.get('featured_only')
            
            if project_type:
                queryset = queryset.filter(project_type=project_type)
            if status:
                queryset = queryset.filter(status=status)
            if featured_only:
                queryset = queryset.filter(is_featured=True)
        
        return queryset.order_by('-order', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ProjectFilterForm(self.request.GET)
        context['project_types'] = Project.PROJECT_TYPE_CHOICES
        context['status_choices'] = Project.STATUS_CHOICES
        return context

class ProjectDetailView(DetailView):
    """Detailed project view"""
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'
    
    def get_object(self, queryset=None):
        return get_object_or_404(Project, slug=self.kwargs['slug'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related projects
        project = self.get_object()
        related_projects = Project.objects.filter(
            project_type=project.project_type
        ).exclude(id=project.id)[:3]
        context['related_projects'] = related_projects
        return context

class SkillsView(ListView):
    """Enhanced skills view with categorization"""
    model = Skill
    template_name = 'skills.html'
    context_object_name = 'skills'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Group skills by category
        skills_by_category = {}
        for skill in self.get_queryset():
            category = skill.get_category_display()
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(skill)
        
        context['skills_by_category'] = skills_by_category
        context['total_skills'] = self.get_queryset().count()
        context['featured_skills'] = self.get_queryset().filter(is_featured=True)
        
        return context

class ContactView(SuccessMessageMixin, CreateView):
    """Enhanced contact view with better UX"""
    model = ContactMessage
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = reverse_lazy('contact')
    success_message = "Thank you for your message! I'll get back to you within 24 hours."
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add contact information
        context['contact_info'] = {
            'email': 'kevin.kimutai@example.com',
            'linkedin': 'https://linkedin.com/in/kevinkimutai',
            'github': 'https://github.com/kevinkimutai',
            'location': 'Nairobi, Kenya',
        }
        return context

# API Views for AJAX functionality
@require_http_methods(["GET"])
def api_projects(request):
    """API endpoint for projects data"""
    projects = Project.objects.filter(status='completed').values(
        'title', 'description', 'project_type', 'technologies', 
        'github_url', 'live_url', 'image'
    )[:10]
    return JsonResponse({'projects': list(projects)})

@require_http_methods(["GET"])
def api_skills(request):
    """API endpoint for skills data"""
    skills = Skill.objects.filter(is_featured=True).values(
        'name', 'category', 'proficiency', 'years_experience'
    )
    return JsonResponse({'skills': list(skills)})

