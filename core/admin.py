from django.contrib import admin
from .models import WorkSample, Client

# REGISTERS
@admin.register(WorkSample)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    

# REGISTERS
@admin.register(Client)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone']
