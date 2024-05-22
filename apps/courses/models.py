from django.db import models
from django.contrib.auth import get_user_model
from ext.choices import LEVEL
from apps.profiles.models import UserProfile

# Create your models here.

User = get_user_model()


class CategoryModel(models.Model):
    category = models.CharField(max_length=100, unique=True)
    
    def __str__(self) -> str:
        return self.category
    
    def save(self, *args, **kwargs) -> None:
        self.category = self.category.lower()
        super().save(*args, **kwargs)
    

class CoursesModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    level = models.CharField(max_length=100, choices=LEVEL)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    preview_image = models.ImageField(upload_to="preview/images/")
    preview_video = models.FileField(upload_to="preview/videos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
    

class CourseItemModel(models.Model):
    course = models.ForeignKey(CoursesModel, on_delete=models.CASCADE, related_name="course_item")
    name = models.CharField(max_length=100, unique=True)
    course_file = models.FileField(upload_to="course/")
    description = models.TextField(blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.course_id} - {self.name}"