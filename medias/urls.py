from django.urls import path

from .views import media_add

urlpatterns = [
    path('story-add', media_add, name='media-add'),
]