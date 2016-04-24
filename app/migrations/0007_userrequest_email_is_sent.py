# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-24 07:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20160420_0722'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrequest',
            name='email_is_sent',
            field=models.BooleanField(default=False, help_text='Thist request was sent without errors', verbose_name='Was sent'),
        ),
    ]
