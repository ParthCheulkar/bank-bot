from django.shortcuts import render, redirect
from django.http import HttpResponse 
# from bankbot.actions.actions import ActionBankBalance
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..models import *
def index(request):
    # abb = ActionBankBalance()
    # abb.checkuser(request.user)
    return render(request, "base.html")

def account_no(request):
    return render(request, "account_no.html")

def video(request):
    return render(request, "video.html")

@login_required(login_url='login')
def profile(request):
    cust_profile = CustomerProfile.objects.get(prof_for=request.user)
    account = Account.objects.get(acc_for = cust_profile)
    # print(cust_profile)
    context = {
        'cust_profile': cust_profile,
        'account': account
    }
    return render(request, "profile.html", context)

def loan(request):
    return render(request, "loan.html")
    
def get_user(request):
    user = request.user

    return JsonResponse({"username":user.username})


def transfermoney(request):
    return render(request, "transfer_money.html")

def insurance(request):
    return render(request, "insurance.html")
    
def cardRequest(request):
    return render(request, "card.html")