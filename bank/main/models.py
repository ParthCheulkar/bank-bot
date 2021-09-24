import random

from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save

from django.utils import timezone


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
    acc_bal = models.DecimalField(max_digits=12, decimal_places=4)
    acc_type = models.CharField(choices=ACCOUNT_TYPES, max_length=50)

    def __str__(self):
        return f"{self.acc_no} - {self.acc_for.f_name}"


TRANSACTION_STATUS = [
    ('successful', 'successful'),
    ('failed', 'failed')
]

TRANSACTION_TYPE = [
    ('IMPS', 'IMPS')
]


class Transaction(models.Model):
    transaction_type = models.CharField(choices=TRANSACTION_TYPE,max_length=50)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver')
    amount = models.DecimalField(max_digits=7, decimal_places=4)
    trxn_date = models.DateField(default=timezone.now)
    trxn_time = models.TimeField(auto_now=True)
    status = models.CharField(choices=TRANSACTION_STATUS,max_length=50)
    remark = models.TextField(blank=True, null=True)

class ImageUpload(models.Model):
    file = models.FileField(upload_to = 'images/')
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.prof_for.username + " Image doc."

class VideoUpload(models.Model):
    file = models.FileField(upload_to = 'videos/')
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.prof_for.username + " Video doc."

class IdUpload(models.Model):
    file = models.FileField(upload_to = 'ids/')
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.prof_for.username + " ID doc."

CARD_TYPE = [
    ('DEB', 'DEBIT'),
    ('CRE', 'CREDIT'),
    ('FRX', 'FOREX'),
]

class CardRequest(models.Model):
    card_for = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    card_type = models.CharField(choices = CARD_TYPE, max_length=50)
    holder_name = models.CharField(max_length=150)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Card For {self.holder_name}"
    


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
            acc_bal = 1000.0000,
            acc_for = instance,
            acc_type = 'SAV'
        )

        instance.prof_for = create_user
        instance.save()

        if create_account:
            f= open(f"../bank/bankbot/data/{username}.txt","w+")
            f.write(f"{create_account.acc_no}\n{instance.cust_crn_no}\n{create_account.acc_bal}")
            f.close()



