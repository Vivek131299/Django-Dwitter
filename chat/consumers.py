import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Chat, Group
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(args, kwargs)
    #     self.room_name = None
    #     self.room_group_name = None
    #     self.room = None
    #     self.user = None
    #     self.user_inbox = None

    def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['groupname']
        # self.room_group_name = f'chat_{self.room_name}'
        # self.room = Room.objects.get(name=self.room_name)
        # self.user = self.scope['user']
        # self.user_inbox = f'inbox_{self.user.username}'

        self.group_name = self.scope['url_route']['kwargs']['groupname']
        # connection has to be accepted

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        print(self.group_name)
        if Group.objects.filter(name=self.group_name).first() is None:
            group = Group(name=self.group_name)
            group.save()


        self.accept()

        # send the user list to the newly joined user
        # self.send(json.dumps({
        #     'type': 'user_list',
        #     'users': [user.username for user in self.room.online.all()],
        # }))
        #
        # if self.user.is_authenticated:
        #     # create a user inbox for private messages
        #     async_to_sync(self.channel_layer.group_add)(
        #         self.user_inbox,
        #         self.channel_name,
        #     )
        #
        #     # send the join event to the room
        #     async_to_sync(self.channel_layer.group_send)(
        #         self.room_group_name,
        #         {
        #             'type': 'user_join',
        #             'user': self.user.username,
        #         }
        #     )
        #     self.room.online.add(self.user)

    def disconnect(self, close_code):
        print('Websocket Disconnected...', close_code)
        print("Channel Layer", self.channel_layer)
        print("Channel Name", self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )


    def receive(self, text_data=None, bytes_data=None):
        group = Group.objects.get(name=self.group_name)
        print(group)
        text_data_json = json.loads(text_data)
        message = text_data_json['msg']
        sender = text_data_json['sender']
        sender_user = User.objects.get(username=sender)
        print(message)

        if self.scope['user'].is_authenticated:
            chat = Chat(
                content=message,
                group=group,
                sender=sender_user
            )
            chat.save()

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat.message',
                'message': message,
                'sender': sender
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def user_join(self, event):
        self.send(text_data=json.dumps(event))

    def user_leave(self, event):
        self.send(text_data=json.dumps(event))

    def private_message(self, event):
        self.send(text_data=json.dumps(event))

    def private_message_delivered(self, event):
        self.send(text_data=json.dumps(event))

