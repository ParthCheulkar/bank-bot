from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import models as userModel
from django.contrib.auth.models import User
from django.contrib import messages
import requests
import json

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        clientKey = request.POST['g-recaptcha-response']
        secretKey = '6LflYjAcAAAAAE-bUmclzdBeRAKPENwkQf9RunXt'

        captchaData = {
            'secret': secretKey,
            'response': clientKey
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        
        if not response['success']:
            messages.info(request, 'Please verify that you are a human')
            return redirect("login")

        user = userModel.auth.authenticate(username=username, password=password)
        
        if user is not None:
            userModel.auth.login(request, user)
            
            return redirect("profile")
        else:
            messages.info(request, 'invalid details')
            return redirect("login")
    else:
        return render(request, "login.html")
    return render(request, "login.html")

def logout(request):
    userModel.auth.logout(request)
    return redirect('login')