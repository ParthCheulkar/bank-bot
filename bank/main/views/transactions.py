from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse 
from ..models import * 
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from decimal import Decimal


def index(request):
    return HttpResponse("hey")



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
            try:
                print(f"moneyy->{user_account.acc_bal}")
                receiver.acc_bal += amount
                user_account.acc_bal -= amount

                receiver.save()
                user_account.save()

                Transaction.objects.create(transaction_type = 'IMPS', sender = user_account, receiver = receiver, amount = amount, status = 'successful', remark=remark)


                messages.success(request, "Transaction success.")
                return render(request, "transfer_money.html")
            except:
                messages.error(request, "Transaction failed.")
                return render(request, "transfer_money.html")
        else:
            messages.error(request, "You dont have enough balance.")
            return render(request, "transfer_money.html")
    else:
        return render(request, "transfer_money.html")