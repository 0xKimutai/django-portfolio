from django import forms
from . models import ContactMessage

class contactForm(forms.Form):
    name = forms.CharField(
        max_length=100, 
        label="Your Name",
        widget=forms.TextInput(attrs={'placeholder': 'John Doe'}),
        )
    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(attrs={'placeholder': 'johndoe12@gmail.com'}),
        )
    message = forms.CharField(
        label="Compose message",
        widget=forms.Textarea(attrs={'placeholder': 'Your message'}),
        )