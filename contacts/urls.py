from django.urls import path
from . import views

urlpatterns = [
    path('', views.contacts, name='contacts'),
    path('chat/submit/', views.chat_submit, name='chat_submit'),
]
