from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse

def index(request):
    return render(request, "base.html")

def account_no(request):
    return render(request, "account_no.html")

def video(request):
    return render(request, "video.html")

def profile(request):
    return render(request, "profile.html")

def loan(request):
    return render(request, "loan.html")
    
def get_user(request):
    user = request.user

    return JsonResponse({"username":user.username})


def transfermoney(request):
    return render(request, "transfer_money.html")

def insurance(request):
    return render(request, "insurance.html")