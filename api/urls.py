from django.urls import path
from . import views


urlpatterns = [
    path('', views.hello, name='home'),
    path('follow/<int:id>/', views.follow, name='follow'),
    path('unfollow/<int:id>/', views.unfollow, name='unfollow'),
    path('dweet/<int:id>/', views.dweet_detail, name='dweet_detail'),
    path('dweet/add/', views.add_dweet, name='add_dweet'),
    path('dweet/delete/<int:id>/', views.delete_dweet, name='delete_dweet'),
    path('dweet/like/<int:id>/', views.like_unlike_dweet, name='like_dweet'),
    path('dweet/comment/<int:id>/', views.add_comment, name='add_comment'),
    path('dweets/all/', views.get_all_dweets, name='get_all_dweets'),
    path('dweets/followed/', views.get_followed_dweets, name='get_followed_dweets'),
    path('profile/', views.display_profile, name='profile'),
    path('profile/<int:id>/', views.display_profile, name='profile'),
]