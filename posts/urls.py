from django.urls import path

from posts.views import *

urlpatterns = [
    path('post-add', post_add, name='post-add'),
    path('post-edit/<int:post_id>', post_edit, name='post-edit'),
    path('api/create', post_create, name='post-create'),
    path('api/update/<post_id>', post_update, name='post-update'),
    path('api/delete/<post_id>', post_delete, name='post-create'),
]
