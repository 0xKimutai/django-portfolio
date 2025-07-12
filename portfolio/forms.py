from django import forms
from django.core.validators import EmailValidator
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    """Enhanced contact form for professional inquiries"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'company', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@company.com',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project Inquiry / Job Opportunity / Collaboration',
                'required': True
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Company (Optional)'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 123-4567 (Optional)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell me about your project, requirements, or how I can help...',
                'rows': 6,
                'required': True
            })
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        validator = EmailValidator()
        try:
            validator(email)
        except forms.ValidationError:
            raise forms.ValidationError("Please enter a valid email address.")
        return email
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and len(message.strip()) < 10:
            raise forms.ValidationError("Please provide a more detailed message (at least 10 characters).")
        return message

class ProjectFilterForm(forms.Form):
    """Form for filtering projects"""
    PROJECT_TYPE_CHOICES = [
        ('', 'All Types'),
        ('web_app', 'Web Application'),
        ('api', 'API/Backend Service'),
        ('mobile', 'Mobile Application'),
        ('data_science', 'Data Science/AI'),
        ('devops', 'DevOps/Infrastructure'),
        ('open_source', 'Open Source'),
        ('research', 'Research Project'),
    ]
    
    STATUS_CHOICES = [
        ('', 'All Status'),
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('maintenance', 'Under Maintenance'),
    ]
    
    project_type = forms.ChoiceField(
        choices=PROJECT_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    featured_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )