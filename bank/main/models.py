from django.db import models
from django.contrib.auth.models import User


class CustomerProfile(models.Model):
    prof_for = models.ForeignKey(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    init_login = models.BooleanField(default=False)
    aadhar_no = models.CharField(max_length=12)
    pan_no = models.CharField(max_length=10)
    aadhar_reg = models.BooleanField(default=False)
    cust_crn_no = models.CharField(max_length=8)
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    def __str__(self):
        return self.prof_for.username
    

ACCOUNT_TYPES = [
    ('SAV','Savings'),
    ('CUR', 'Current'),
    ('FD', 'Fixed Deposit'),
    ('RD', 'Recurring Deposit')
]

class Account(models.Model):
    acc_for = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    acc_no = models.CharField(max_length=10)
    acc_bal = models.DecimalField(max_digits=7, decimal_places=4)
    acc_type = models.CharField(choices=ACCOUNT_TYPES, max_length=50)

    def __str__(self):
        return self.acc_no
    


