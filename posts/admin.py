from django.contrib import admin

from .models import Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'user_tag', 'post_date', 'img')

    def user_tag(self, obj):
        return f"{obj.user.name} ({obj.user.tag})"
    user_tag.short_description = 'User'


admin.site.register(Post, PostAdmin)
