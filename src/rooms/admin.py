from django.contrib import admin

from rooms.models import Room, RoomData


class RoomInline(admin.TabularInline):
    model = Room
    extra = 0
    show_change_link = True


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'status', 'is_available']
    readonly_fields = ['updated', 'created']
    search_fields = ['number']
    list_filter = ['status', 'is_available']


@admin.register(RoomData)
class RoomDataAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'type', 'persons', 'single_beds', 'double_beds', 'price']
    prepopulated_fields = {'slug': ['name']}
    readonly_fields = ['updated', 'created']
    search_fields = ['name', 'slug']
    list_filter = ['type', 'single_beds', 'double_beds']
    inlines = [RoomInline]

    @staticmethod
    def persons(instance):
        return instance.persons
