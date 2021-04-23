from django.contrib import admin

from medias.models import Media
from posts.models import Post
from .models import *

admin.site.register(User)
admin.site.register(Media)
admin.site.register(Post)

