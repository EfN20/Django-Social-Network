from django.urls import path

from posts.views import PostAddView, PostEditView

urlpatterns = [
    path('post-add', PostAddView, name = 'post-add'),
    path('post-edit/<int:post_id>', PostEditView, name = 'post-edit'),

]