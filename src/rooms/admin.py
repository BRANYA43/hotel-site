from django.contrib import admin

from rooms.models import Number, Room


class NumberInline(admin.TabularInline):
    model = Number
    extra = 0


@admin.register(Number)
class NumberAdmin(admin.ModelAdmin):
    list_display = ['number', 'room', 'is_available']
    fields = ['number', 'room', 'is_available']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['slug', 'type', 'status', 'price', 'single_beds', 'double_beds']
    fields = ['slug', 'type', 'status', 'price', 'single_beds', 'double_beds']
    inlines = [NumberInline]
