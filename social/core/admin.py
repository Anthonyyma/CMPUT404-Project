from core.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    # display the profile_image in the admin panel for users
    fieldsets = ((None, {"fields": ("profile_image",)}), *BaseUserAdmin.fieldsets)


# Register your models here.
admin.site.register(User, UserAdmin)
