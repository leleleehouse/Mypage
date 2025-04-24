from django.contrib import admin
from .models import Project, TechStack, ContactMessage
# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['title']
    
class ContactMessageAdmin(admin.ModelAdmin):
    search_fields = ['title']
    
admin.site.register(Project, ProjectAdmin)
admin.site.register(TechStack)
admin.site.register(ContactMessage, ContactMessageAdmin)