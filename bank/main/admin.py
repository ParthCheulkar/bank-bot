from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display=['id','prof_for','phone','email']

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display=['id','acc_no','acc_for','acc_type', 'acc_bal']