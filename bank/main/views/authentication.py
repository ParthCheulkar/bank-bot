from django.shortcuts import render, redirect
from django.http import HttpResponse 

def login(request):
    return render(request, "login.html")
