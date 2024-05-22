from django.contrib import admin
from .models import CoursesModel, CourseItemModel, CategoryModel

# Register your models here.

admin.site.register(CoursesModel)
admin.site.register(CourseItemModel)
admin.site.register(CategoryModel)