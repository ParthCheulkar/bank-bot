from django.shortcuts import render, redirect
from django.http import HttpResponse 

def chatroom(request):
    return render(request, "chatroom.html")