from django.contrib import admin

from .models import Media


class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'text', 'posted_date', 'user_tag')

    def user_tag(self, obj):
        return f"{obj.user.name} ({obj.user.tag})"
    user_tag.short_description = 'User'


admin.site.register(Media, MediaAdmin)
