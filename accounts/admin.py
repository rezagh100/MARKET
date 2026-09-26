from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_staff', 'phone_number']
    model = User

    fieldsets = UserAdmin.fieldsets + (
        ('Personal info', {'fields': ('phone_number',)}),
    )


admin.site.register(User, CustomUserAdmin)
