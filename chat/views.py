from django.shortcuts import render
# from chat.models import Room
from api.models import Profile
from .models import Chat, Group


# def index_view(request):
#     return render(request, 'room_index.html', {'rooms': Room.objects.all()})


# def room_view(request, room_name):
#     chat_room, created = Room.objects.get_or_create(name=room_name)
#     return render(request, 'chat.html', {'room': chat_room})


def chat_view(request, id):
    profile = Profile.objects.get(id=id)

    group = Group.objects.filter(name=group_name).first()
    chats = []
    if group:
        chats = Chat.objects.filter(group=group)
    else:
        group = Group(name=group_name)
        group.save()

    return render(request, 'chat.html', {'profile': profile})
