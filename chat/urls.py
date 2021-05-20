from django.urls import path

from .views import chat_page, chat_by_id, chat_by_name

urlpatterns = [
    path('', chat_page, name='chat-page'),
    path('private/<str:room_name>/', chat_by_name, name='private_chat'),
    path('<int:room_id>/', chat_by_id, name='single-chat-id'),
]
