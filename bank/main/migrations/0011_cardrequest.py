# Generated by Django 3.2.7 on 2021-09-24 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_idupload_imageupload_videoupload'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_type', models.CharField(choices=[('DEB', 'DEBIT'), ('CRE', 'CREDIT'), ('FRX', 'FOREX')], max_length=50)),
                ('holder_name', models.CharField(max_length=150)),
                ('card_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customerprofile')),
            ],
        ),
    ]
