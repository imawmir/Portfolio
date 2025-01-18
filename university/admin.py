# IMPORTS
from django.contrib import admin
from . models import News, Course, Enroll


# REGISTERS
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at']
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']

@admin.register(Enroll)
class EnrollAdmin(admin.ModelAdmin):
    list_display = ['id', 'firstname', 'lastname', 'major']