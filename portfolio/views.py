from django.shortcuts import render, redirect
from django.contrib import messages
from . models import Project, Skill, Education
from . forms import contactForm

#Create your views here

def index(request):
    projects = Project.objects.all()
    skills = Skill.objects.all()
    education = Education.objects.all()
    form = contactForm(request.POST or None)
    success = False

    if request.method == "POST" and form.is_valid():
        messages.success(request, 'Thank you for your message!')
        return redirect('index')

    context ={
        'projects': projects,
        'skills': skills,
        'education': education,
        'form': form,
        
    }

    return render(request, 'index.html', context)