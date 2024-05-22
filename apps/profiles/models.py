from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class UserProfile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    photo = models.ImageField(upload_to="uploads/", blank=True)
    description = models.TextField(blank=True, null=True)
    contacts = models.CharField(max_length=40, blank=True, null=True)
    youtube_url = models.CharField(max_length=100, null=True, blank=True, help_text="Link to owners youtube")
    linkedin_url = models.CharField(max_length=100, null=True, blank=True, help_text="Link to owners linked in")
    github_url = models.CharField(max_length=100, null=True, blank=True, help_text="Link to owners github")
    
    def __str__(self) -> str:
        return self.username