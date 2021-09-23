from django.urls import path
from .views import authentication, main

urlpatterns = [
    path('', main.index, name="base"),
    path('login/', authentication.login, name="login"),
    path('login/account_no', main.account_no, name="account_no"),
    path('login/video', main.video, name="video"),
]
