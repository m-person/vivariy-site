# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-04 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20160704_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analyticscounter',
            name='code',
            field=models.TextField(default='', help_text='Counter code. Copy there code, provided by service (google, yandex).                                 Code should be js string like "&ltscript&gt...&lt/script&gt"', max_length=20000, verbose_name='Code'),
        ),
    ]
