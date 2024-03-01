from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path(r'ws/chat/<str:groupname>/', consumers.ChatConsumer.as_asgi()),
]

