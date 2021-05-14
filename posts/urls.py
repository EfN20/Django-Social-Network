from django.urls import path

from posts.views import post_add, post_edit

urlpatterns = [
    path('post-add', post_add, name='post-add'),
    path('post-edit/<int:post_id>', post_edit, name='post-edit'),

]
