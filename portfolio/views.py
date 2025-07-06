from django.shortcuts import render, redirect
from django.contrib import messages
from . models import Project, Skill,ContactMessage
from . forms import contactForm

#Create your views here

def index(request):
    projects = Project.objects.all()
    skills = Skill.objects.all()
    form = contactForm(request.POST or None)
    success = False

    context ={
    'projects': projects,
    'skills': skills,
    'form': form,
    
    }

    return render(request, 'index.html', context)

def home (request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects.html')

def skills(request):
    skills = Skill.objects.all()
    return render(request, 'skills.html', {'skills': skills})

def contact(request):
    form = contactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        #Save to db
        ContactMessage.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            message=form.cleaned_data['message']
        )

        messages.success(request, 'Thank you for your message!')
        return redirect('contact')
    return render(request, 'contact.html', {'form': form})