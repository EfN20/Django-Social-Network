from django.contrib import admin

from .models import Room, Message


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room_name_id', 'text', 'date')

    def room_name_id(self, obj):
        return f"{obj.room.name} ({obj.room.id})"
    room_name_id.short_description = 'room'


admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
