from django.contrib import admin
from django.contrib.auth import get_user_model

from accounts.models import Profile

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'is_active', 'is_confirmed_email', 'is_staff', 'is_superuser', 'groups', 'last_login', 'joined']
    readonly_fields = ['last_login', 'joined']
    inlines = [ProfileInline]
