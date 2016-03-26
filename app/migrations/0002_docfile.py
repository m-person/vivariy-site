# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-22 09:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(help_text='File title (in english)', max_length=128, verbose_name='Title (en)')),
                ('title_ru', models.CharField(help_text='File title (in russian)', max_length=128, verbose_name='Title (ru)')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Don`t show it on site')),
                ('file', models.FileField(upload_to='doc_files/', verbose_name='File')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doc_files', to='app.Product')),
            ],
            options={
                'verbose_name': 'Doc file',
                'verbose_name_plural': 'Doc files',
            },
        ),
    ]
