
from django.shortcuts import render, redirect
from django.http import HttpResponse 
from bankbot.actions.actions import ActionBank
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse
from ..models import * 
from twilio.rest import Client
from django.contrib import messages

from django.contrib.auth import models as userModel
import os

from .ml import *

def index(request):
    abb = ActionBank()
    abb.checkuser(request.user)
    return render(request, "base.html")

def account_no(request):
    if request.method == "POST":
        acc_no = request.POST["accno"]
        print(acc_no)
        try:
            user_acc = Account.objects.get(acc_no=acc_no)
            print(f"f-user-ac->{user_acc}")
            return redirect(f"/video/{acc_no}/")
        except:
            messages.error(request, "User Dosent exist")
            return redirect("account_no")
    return render(request, "account_no.html")

import base64
import glob
@csrf_exempt
def video(request, accno):
    acc_no = accno
    print(f"vid->acc->{acc_no}")
    user = Account.objects.get(acc_no=acc_no).acc_for.prof_for
    print(f"vid->use->{user}")
    print(f"vid->use->{user.username}")
    if request.method == "POST":
        vid = request.FILES.get('video')
        text = base64.b64encode(vid.read())
        fh = open(f"../bank/media/videos/{user.username}_video.mp4", "wb")
        fh.write(base64.b64decode(text))
        fh.close()
        flag = 1
        # try:
        flag = verification(user.username)
        # except:
        #     pass
        if flag == 0:
            prof = CustomerProfile.objects.get(prof_for=user)
            prof.init_login = True
            prof.save()

            ss_files = glob.glob(f"../bank/main/vid_ss/{user.username}/*")
            # print(f"ss_fls->{ss_files}")
            for f in ss_files:
                os.remove(f)
            # os.remove(f"../ekyc/main/vid_ss/{request.user.username}")
            return JsonResponse({"mssg": "success", "redUrl": f'/crnsent/{accno}/'})
            # return redirect(f'/crnsent/{accno}/')
        else:
            os.remove(f"../bank/main/vid_ss/{user.username}")
            return JsonResponse({"mssg": "fail"})
            # mssg = "Please recheck your uploaded documents and ensure that there is proper lighting for the video. There was some problem in processing your request."
            # return render(request, 'documents.html', {"message":mssg})
        # vid_final = VideoUpload(file=base64.b64decode(text), user=request.user)
        # vid_final.save()
    else:
        return render(request, 'video.html')

def crn_sent(request, accno):
    user_prof = Account.objects.get(acc_no=accno).acc_for
    
    phone = user_prof.phone
    account_sid = "AC703679e4bfdc618b2c00d92b79be454c"
    # Your Auth Token from twilio.com/console
    auth_token  = "39bbacefcaf41a2fec45e9d377ab1f71"

    client = Client(account_sid, auth_token)

    print(f"you crn->{user_prof.cust_crn_no}")
    print(f"you phone->{user_prof.phone}")
    message = client.api.account.messages.create(
        to=phone, 
        from_="+15743672651",
        body=f"Your CRN is: {user_prof.cust_crn_no}")
    
    return render(request, "login.html", {"mssg":"Your CRN is sent."})

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