from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.urls import reverse

def get_default_created_time():
    return timezone.now()

class Skill(models.Model):
    """Enhanced skill model for senior engineer portfolio"""
    CATEGORY_CHOICES = [
        ('backend', 'Backend Development'),
        ('frontend', 'Frontend Development'),
        ('devops', 'DevOps & Infrastructure'),
        ('database', 'Database & Data Engineering'),
        ('ai_ml', 'AI & Machine Learning'),
        ('cloud', 'Cloud Platforms'),
        ('testing', 'Testing & Quality Assurance'),
        ('tools', 'Development Tools'),
        ('soft_skills', 'Soft Skills'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='backend')
    proficiency = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Skill proficiency level (0-100)"
    )
    years_experience = models.DecimalField(
        max_digits=3, 
        decimal_places=1,
        default=0.0,
        help_text="Years of experience with this skill"
    )
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['category', 'order', '-proficiency']
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Experience(models.Model):
    """Professional experience model"""
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('consulting', 'Consulting'),
    ]
    
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    achievements = models.JSONField(default=list, help_text="List of key achievements")
    technologies_used = models.JSONField(default=list, help_text="List of technologies used")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-start_date', 'order']
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    @property
    def duration(self):
        """Calculate duration of employment"""
        end = self.end_date or timezone.now().date()
        return end - self.start_date

class Project(models.Model):
    """Enhanced project model with more details"""
    PROJECT_TYPE_CHOICES = [
        ('web_app', 'Web Application'),
        ('api', 'API/Backend Service'),
        ('mobile', 'Mobile Application'),
        ('data_science', 'Data Science/AI'),
        ('devops', 'DevOps/Infrastructure'),
        ('open_source', 'Open Source'),
        ('research', 'Research Project'),
    ]
    
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('maintenance', 'Under Maintenance'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    detailed_description = models.TextField(blank=True)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES, default='web_app')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    technologies = models.JSONField(default=list, help_text="List of technologies used")
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    demo_url = models.URLField(blank=True, null=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=get_default_created_time)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Certification(models.Model):
    """Professional certifications model"""
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    credential_id = models.CharField(max_length=100, blank=True)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='certifications/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"

class ContactMessage(models.Model):
    """Enhanced contact message model"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    company = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-sent_at']
    
    def __str__(self):
        return f'{self.name} ({self.email}) - {self.subject}'

class Education(models.Model):
    """Education background model"""
    DEGREE_CHOICES = [
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('phd', 'PhD'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    ]
    
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    field_of_study = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-end_date', '-start_date']
    
    def __str__(self):
        return f"{self.get_degree_display()} in {self.field_of_study} - {self.institution}"