# Generated by Django 3.2.7 on 2021-09-23 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_transaction_receiver'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='trxn_time',
            field=models.TimeField(auto_now=True),
        ),
    ]
