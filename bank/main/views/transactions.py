from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from ..models import * 
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from decimal import Decimal
from django.core import serializers

import random
from twilio.rest import Client


def index(request):
    return HttpResponse("hey")

def generate_otp(request):
    otp = random.randint(1111,9999) 
    request.session["otp"] = otp 
    print(f"genotp->{otp}")
    phone = CustomerProfile.objects.get(prof_for = request.user).phone
    account_sid = "AC703679e4bfdc618b2c00d92b79be454c"
    # Your Auth Token from twilio.com/console
    auth_token  = "39bbacefcaf41a2fec45e9d377ab1f71"

    client = Client(account_sid, auth_token)

    message = client.api.account.messages.create(
        to=phone, 
        from_="+15743672651",
        body=f"Your OTP is: {otp}")
    return otp


def verify_otp(request):
    
    if request.method == 'POST':
        ist = request.POST['ist']
        sec = request.POST['sec']
        third = request.POST['third']
        fourth = request.POST['fourth']

        digits = ist+sec+third+fourth

        otp = request.session["otp"]

        
        print(f"otp->{otp}")

        rname = request.session["rname"]
        accountno = request.session["accountno"]
        amount = Decimal(request.session["amount"])
        remark = request.session["remark"]
        print(f"rname->{rname}")
        print(f"accountno->{accountno}")
        print(f"remark->{remark}")
        print(f"amount->{amount}")

        user = request.user
        # user = User.objects.get(username="Shyren@473793737284")
        user_account = Account.objects.get(acc_for=CustomerProfile.objects.get(prof_for=user))
        receiver = Account.objects.get(acc_no = accountno)
        if int(digits) == otp:
            # try:
            print(f"moneyy->{user_account.acc_bal}")
            
            receiver.acc_bal += amount
            user_account.acc_bal -= amount

            receiver.save()
            user_account.save()

            Transaction.objects.create(transaction_type = 'IMPS', sender = user_account, receiver = receiver, amount = amount, status = 'successful', remark=remark)
            f = open(f"../bank/bankbot/data/{request.user.username}.txt","w+")
            f.write(f"{user_account.acc_no}\n{user_account.acc_for.cust_crn_no}\n{user_account.acc_bal}")
            f.close()
            f2 = open(f"../bank/bankbot/data/data.txt","w+")
            f2.write(f"{user_account.acc_no}\n{user_account.acc_for.cust_crn_no}\n{user_account.acc_bal}")
            f2.close()
            messages.success(request, "Transaction success.")
            return render(request, "transfer_money.html")
            # except:
            #     messages.error(request, "Transaction failed.")
            #     return render(request, "transfer_money.html")
        else:
            messages.error(request, "OTP did not match.")
            
            return redirect('verifyotp')
    else:
        return render(request, 'otp.html')


@csrf_exempt
def get_transactions(request):
    user = request.user
    # user = User.objects.get(username="Shyren@473793737284")
    user_account = Account.objects.get(acc_for=CustomerProfile.objects.get(prof_for=user))
    transactions = Transaction.objects.filter(Q(sender=user_account) | Q(receiver=user_account))
    # for transaction in transactions:
    #     if transaction.sender == user_account:
    #         print(f"red {transaction.amount}")
    #     else:
    #         print(f"green {transaction.amount}")
    
    return render(request, 'account_activity.html', {"transactions":transactions, "user_account":user_account})

@csrf_exempt
def get_transactions_json(request):
    user = request.user
    user_account = Account.objects.get(acc_for=CustomerProfile.objects.get(prof_for=user))
    transactions = Transaction.objects.filter(Q(sender=user_account) | Q(receiver=user_account))
    transactions_json = serializers.serialize("json", transactions)
    # print(transactions_json)
    return JsonResponse(transactions_json, safe=False)

def make_transaction(request):
    user = request.user

    user_account = Account.objects.get(acc_for=CustomerProfile.objects.get(prof_for=user))

    if request.method == "POST":
        rname = request.POST["rname"]
        accountno = request.POST["accountno"]
        amount = Decimal(request.POST["amount"])
        remark = request.POST["remark"]


        receiver = Account.objects.get(acc_no = accountno)
        print(f"reci->{receiver.acc_no}")
        print(f"sender->{user_account.acc_no}")
        if user_account.acc_bal > amount+Decimal(100.0):
            generate_otp(request)
            request.session["rname"] = rname
            request.session["accountno"] = accountno
            request.session["amount"] = str(amount)
            request.session["remark"] = remark
            
            return redirect("verifyotp")

        else:
            messages.error(request, "You dont have enough balance.")
            return render(request, "transfer_money.html")
    else:
        return render(request, "transfer_money.html")

def autosuggest(request):
    # print(request.GET)
    # <QueryDict: {'term': ['gh']}>
    query_original = request.GET.get('term')
    # queryset = Products.objects.filter(title__icontains=query_original)
    queryset = Transaction.objects.filter(Q(sender__acc_no__startswith = query_original) | Q(receiver__acc_no__startswith = query_original))
    # returning json resp
    # putting title of queryset in list
    mylist = []

    # x = prodcutObj.title
    mylist += [x.sender.acc_no for x in queryset]
    mylist.sort()
    return JsonResponse(mylist, safe=False)

def get_transactions_search(request):
    query_original = request.GET.get('term')
    account = Account.objects.get(acc_no=query_original)

    user = request.user
    user_account = Account.objects.get(acc_for=CustomerProfile.objects.get(prof_for=user))
    transactions = Transaction.objects.filter(Q(sender=user_account) | Q(receiver=user_account))
    transactions = transactions.filter((Q(sender=user_account) & Q(receiver=account)) | (Q(sender=account) & Q(receiver=user_account)))
    # transactions = transactions.filter(Q(sender=account) | Q(receiver=account))
    # print(transactions)
    # queryset = Transaction.objects.get(sender__acc_no = query_original)

    # transactions = []

    # x = prodcutObj.title
    # transactions += [x.sender.acc_no for x in queryset]
    
    return render(request, 'account_activity.html', {"transactions": transactions, "user_account": user_account})
    
def verifyotp(request):
    return render(request, "otp.html")