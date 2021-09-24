from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import models as userModel
from django.contrib.auth.models import User

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

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
    return redirect('/')