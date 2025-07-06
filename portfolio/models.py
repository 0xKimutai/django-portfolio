from django.db import models

# Create your models here.

class Project(models.Model) :
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__ (self):
        return self.title
    
class Skill(models.Model):
    name = models.CharField(max_length=255)
    proficiency = models.IntegerField(default=0) # e.g., 0-100

    def __str__(self):
        return self.name
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.email})'