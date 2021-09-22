from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save

class CustomerProfile(models.Model):
    prof_for = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=50)
    init_login = models.BooleanField(default=False)
    aadhar_no = models.CharField(max_length=12, blank=True, null=True)
    pan_no = models.CharField(max_length=10, blank=True, null=True)
    aadhar_reg = models.BooleanField(default=False)
    cust_crn_no = models.CharField(max_length=8)
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    address = models.TextField(blank=True)
    dob = models.DateField(blank=True, null=True)

    def __str__(self):
        if self.prof_for.username:
            return self.prof_for.username
        return self.phone
    

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
        return f"{self.acc_no} - {self.acc_for.f_name}"

import random

@receiver(post_save, sender=CustomerProfile)
def post_save_for_customer_profile(sender, instance, created, **kwargs):
    if created:
        username = ""
        if instance.aadhar_reg == True:
            username = instance.f_name + "@" + instance.aadhar_no
        else:
            username = instance.f_name + "@" + instance.pan_no

        ## Creating a user object after cust profile
        create_user, user_created = User.objects.get_or_create(
            username = username,
            password = instance.cust_crn_no,
            email = instance.email
        )
        if user_created:
            create_user.set_password(instance.cust_crn_no)
            create_user.save()

            # cust_prof = CustomerProfile.objects.get(cust_crn_no=instance.cust_crn_no)
            # cust_prof.prof_for = create_user
            # cust_prof.save()
        
        ## Create an account object after cust profile
        create_account, account_created = Account.objects.get_or_create(
            acc_no = random.randint(1111111111, 9999999999),
            acc_bal = 100.0000,
            acc_for = instance
        )

        instance.prof_for = create_user
        instance.save()