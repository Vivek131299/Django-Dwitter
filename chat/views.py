from django.contrib.auth.models import User
from django.shortcuts import render
# from chat.models import Room
from api.models import Profile
from .models import Chat, Group
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


# def index_view(request):
#     return render(request, 'room_index.html', {'rooms': Room.objects.all()})


# def room_view(request, room_name):
#     chat_room, created = Room.objects.get_or_create(name=room_name)
#     return render(request, 'chat.html', {'room': chat_room})


@csrf_exempt
@login_required
def chat_view(request, id, group_name):
    profile = Profile.objects.get(id=id)

    group = Group.objects.filter(name=group_name).first()
    chats = []
    if group:
        chats = Chat.objects.filter(group=group)
    else:
        group = Group(name=group_name)
        group.save()

    return render(request, 'chat.html', {'profile': profile, 'group_name': group_name, 'chats': chats})


class ChatListView:
    def __init__(self, username, profile_id, group_name):
        self.username = username
        self.profile_id = profile_id
        self.group_name = group_name


@csrf_exempt
@login_required
def view_all_chats(request):
    groups = list(Chat.objects.filter(sender=request.user).order_by().values_list('group', flat=True).distinct())
    chat_views = []
    for group_id in groups:
        group_name = Group.objects.get(id=group_id).name
        username = group_name.replace(f"_{request.user}", "").replace(f"{request.user}_", "")
        profile_id = User.objects.get(username=username).profile.id
        chat_views.append(ChatListView(username, profile_id, group_name))

    return render(request, 'all_chats.html', {'chat_views': chat_views})
