from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LocalGuide

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('language_preference', 'profile_picture')}),
    )

@admin.register(LocalGuide)
class LocalGuideAdmin(admin.ModelAdmin):
    list_display = ['user', 'region', 'experience_years', 'hourly_rate', 'rating']
