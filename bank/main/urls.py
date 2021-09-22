from django.urls import path
from .views import authentication, main

urlpatterns = [
    path('', main.index, name="index"),
    path('login/', authentication.login, name="login"),
]
