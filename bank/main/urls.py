from django.urls import path
from .views import authentication, main, chatroom

urlpatterns = [
    path('', main.index, name="base"),
    path('login/', authentication.login, name="login"),
    path('chatroom/', chatroom.chatroom, name="chatroom"),
    path('login/account_no', main.account_no, name="account_no"),
    path('login/video', main.video, name="video"),
    path('profile/', main.profile, name="profile"),
]
