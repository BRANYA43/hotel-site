from django.contrib import admin
from django.contrib.auth import get_user_model

from accounts.forms import UserAdminForm
from accounts.models import Profile

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'email_is_confirmed', 'is_staff', 'is_superuser', 'joined']
    fields = [
        'email',
        'password',
        'is_active',
        'email_is_confirmed',
        'is_staff',
        'is_superuser',
        'groups',
        'last_login',
        'joined',
    ]
    readonly_fields = ['last_login', 'joined']
    list_filter = ['is_active', 'email_is_confirmed', 'is_staff', 'is_superuser']
    inlines = [ProfileInline]
    form = UserAdminForm
