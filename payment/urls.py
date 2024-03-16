from django.urls import path
from . import views

urlpatterns = [
    path('', views.donate, name='donate'),
    path('payment/', views.payment, name='payment'),
    path('payment_handler/', views.payment_handler, name='payment_handler')
]