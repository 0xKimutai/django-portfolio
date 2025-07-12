from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Project, Skill, ContactMessage, Experience, Certification, Education

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'years_experience', 'is_featured', 'order']
    list_filter = ['category', 'is_featured', 'proficiency']
    search_fields = ['name', 'description']
    list_editable = ['proficiency', 'years_experience', 'is_featured', 'order']
    ordering = ['category', 'order', '-proficiency']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'employment_type', 'start_date', 'end_date', 'is_current', 'order']
    list_filter = ['employment_type', 'is_current', 'start_date']
    search_fields = ['title', 'company', 'description']
    list_editable = ['is_current', 'order']
    ordering = ['-start_date', 'order']
    date_hierarchy = 'start_date'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'project_type', 'status', 'is_featured', 'start_date', 'created_at']
    list_filter = ['project_type', 'status', 'is_featured', 'start_date']
    search_fields = ['title', 'description', 'technologies']
    list_editable = ['status', 'is_featured']
    ordering = ['-order', '-created_at']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'detailed_description')
        }),
        ('Project Details', {
            'fields': ('project_type', 'status', 'technologies', 'image')
        }),
        ('Links', {
            'fields': ('github_url', 'live_url', 'demo_url'),
            'classes': ('collapse',)
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date'),
            'classes': ('collapse',)
        }),
        ('Display Options', {
            'fields': ('is_featured', 'order'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuing_organization', 'issue_date', 'expiry_date', 'is_active']
    list_filter = ['is_active', 'issue_date', 'expiry_date']
    search_fields = ['name', 'issuing_organization', 'credential_id']
    list_editable = ['is_active']
    ordering = ['-issue_date']
    date_hierarchy = 'issue_date'

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'field_of_study', 'institution', 'start_date', 'end_date', 'is_current']
    list_filter = ['degree', 'is_current', 'start_date']
    search_fields = ['field_of_study', 'institution', 'description']
    list_editable = ['is_current']
    ordering = ['-end_date', '-start_date']
    date_hierarchy = 'start_date'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'company', 'is_read', 'sent_at']
    list_filter = ['is_read', 'sent_at']
    search_fields = ['name', 'email', 'subject', 'message', 'company']
    list_editable = ['is_read']
    ordering = ['-sent_at']
    readonly_fields = ['sent_at']
    date_hierarchy = 'sent_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'sent_at'),
            'classes': ('collapse',)
        }),
    )
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    actions = ['mark_as_read']

# Customize admin site
admin.site.site_header = "Senior Python Engineer Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Portfolio Administration"