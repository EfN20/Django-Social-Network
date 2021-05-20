from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Room, Message
from users.models import User


@login_required
def chat_page(request):
    context = {
        "rooms": Room.objects.filter(members=request.user)
    }
    return render(request, 'chat/chat-page.html', context)


@login_required
def chat_by_name(request, room_name):
    room, created = Room.objects.get_or_create(name=room_name, type=False)
    ids = room_name.split("_")
    for user_id in ids:
        room.members.add(User.objects.get(id=user_id))
    print(f"[ chat_by_name ] {room.name}")
    context = {
        'room_id': room.id,
        'messages': Message.objects.filter(room=room)
    }
    return render(request, 'chat/single-chat.html', context)


@login_required
def chat_by_id(request, room_id):
    room = Room.objects.get(id=room_id)
    print(f"[ chat_by_id ] {room.name}")
    context = {
        'room_id': room.id,
        'messages': Message.objects.filter(room=room)
    }
    return render(request, 'chat/single-chat.html', context)


# def private_chat(request, to_user_id):
#     room = Room.objects.all()
#     ids = [request.user.id, to_user_id]
#     for need_id in ids:
#         room = room.filter(members__user_id=need_id)
#     if not room:
#         room = Room()
#     context = {
#         'room': room,
#         'messages': Message.objects.filter(room=room)
#     }
#     return render(request, 'chat/single-chat.html', context)
