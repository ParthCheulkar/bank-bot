from django.urls import path
from .views import authentication, main, chatroom

urlpatterns = [
    path('', main.index, name="index"),
    path('login/', authentication.login, name="login"),
    path('chatroom/', chatroom.chatroom, name="chatroom"),
]
