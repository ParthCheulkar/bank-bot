from django.shortcuts import render, redirect
from django.http import HttpResponse 
from bankbot.actions.actions import ActionBankBalance

def index(request):
    abb = ActionBankBalance()
    abb.checkuser(request.user)
    return render(request, "base.html")

def account_no(request):
    return render(request, "account_no.html")

def video(request):
    return render(request, "video.html")

def profile(request):
    return render(request, "profile.html")


