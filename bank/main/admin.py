from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display=['id','prof_for','phone','email']

# admin.site.register(Account)
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display=['id','acc_no','acc_for','acc_type', 'acc_bal']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display=['id', 'sender', 'receiver', 'amount', 'trxn_date', 'trxn_time','status']

admin.site.register(ImageUpload)
admin.site.register(VideoUpload)
admin.site.register(IdUpload)
