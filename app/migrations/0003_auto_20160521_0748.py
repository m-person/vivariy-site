# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-21 07:48
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20160521_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='desc_full_ru',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', help_text='Full device description in russian (20000 symbols max)', max_length=20000, null=True, verbose_name='Full description (ru)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='specifications_ru',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', help_text='Technical characteristics in russian (20000 symbols max)', max_length=20000, null=True, verbose_name='Specifications (ru)'),
        ),
    ]