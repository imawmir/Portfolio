from django.contrib import admin
from .models import Spent, Building


# Building Register
@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'area']


# Spent Register
@admin.register(Spent)
class SpentAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'price', 'date']
