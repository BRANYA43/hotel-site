from django.contrib import admin

from bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'user', 'is_paid', 'check_in', 'check_out', 'created']
    fields = [
        'uuid',
        'user',
        'persons',
        'type',
        'has_children',
        'is_paid',
        'check_in',
        'check_out',
        'rooms',
        'updated',
        'created',
    ]
    readonly_fields = ['uuid', 'updated', 'created']
