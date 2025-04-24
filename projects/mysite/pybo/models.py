from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class TechStack(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField() 
    tech_stack_tag = models.ManyToManyField(TechStack, related_name="projects")
    github_url = models.URLField(blank=True, null=True)
    project_img = models.ImageField(upload_to='img/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} <{self.email}>"
