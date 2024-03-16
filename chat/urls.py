from django.urls import path
from . import views


urlpatterns = [
    # path('', views.index_view, name='room-index'),
    # path('<str:room_name>/', views.room_view, name='room-view'),
    path('all/', views.view_all_chats, name='all_chats'),
    path('<int:id>/<str:group_name>/', views.chat_view, name='chat'),
]
