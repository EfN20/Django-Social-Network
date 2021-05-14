from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from medias.models import Media
from posts.models import Post
from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'name', 'tag', 'email', 'date_of_birth', 'avatar', 'phone_number', 'is_staff', 'is_superuser')
    list_filter = ('is_superuser',)

    add_fieldsets = (
        (None, {'fields': ('name', 'tag', 'email', 'date_of_birth', 'avatar', 'phone_number', 'password', 'is_staff', 'is_superuser',)}),
    )

    fieldsets = (
        (None, {'fields': ('phone_number', 'is_staff', 'is_superuser', 'password')}),
        ('Personal info', {'fields': ('name', 'tag', 'email', 'date_of_birth', 'avatar')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )   

    search_fields = ('phone', 'tag', 'name')
    ordering = ('tag',)
    filter_horizontal = ()


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'user_tag', 'post_date', 'img')

    def user_tag(self, obj):
        return f"{obj.user.name} ({obj.user.tag})"
    user_tag.short_description = 'User'


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Media)
