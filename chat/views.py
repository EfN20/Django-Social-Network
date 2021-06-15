from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView

from .models import Room, Message
from .forms import RoomForm
from users.models import User


@login_required
def chat_page(request):
    form = RoomForm(user=request.user)
    context = {
        "rooms": Room.objects.filter(members=request.user),
        "group_chat_form": form
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


@login_required
def create_group_chat(request):
    print("Create group chat")
    if request.method == 'POST':
        form = RoomForm(request.POST, user=request.user)
        if form.is_valid():
            room = form.save(commit=False)
            members_id = request.POST.getlist('members')
            print(members_id)
            members = User.objects.filter(user_id__in=members_id)
            room.type = True
            room.save()
            room.members.set(members)
            room.members.add(request.user)
            room.save()
            return redirect('chat-page')
