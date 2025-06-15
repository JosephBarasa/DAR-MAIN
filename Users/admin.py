from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # fields in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')                  
    # fields in the user edit form
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Roles & Permissions', {'fields': ('role', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields in the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role')}
        ),
    )
    
    search_fields = ('username', 'email')
    ordering = ('username',)

# Register the CustomUser model


admin.site.register(CustomUser, CustomUserAdmin)
admin.site_header = "VAMS Admin"
admin.site.site_title = "VAMS Dashboard"
admin.site.index_title = "Welcome to the Visual Artists Management System"