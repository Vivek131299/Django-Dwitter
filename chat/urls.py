from django.urls import path
from . import views


urlpatterns = [
    # path('', views.index_view, name='room-index'),
    # path('<str:room_name>/', views.room_view, name='room-view'),
    path('<int:id>/', views.chat_view, name='chat'),
]
