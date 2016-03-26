# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-22 10:52
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(help_text='Category title (in english).', max_length=254, verbose_name='Title (en)')),
                ('title_ru', models.CharField(help_text='Category title (in russian).', max_length=254, verbose_name='Title (ru)')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Don`t show this entry on site')),
            ],
            options={
                'verbose_name_plural': 'Product categories',
                'verbose_name': 'Product category',
            },
        ),
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(blank=True, help_text='Just to distinguish one image from another. It isn`t necessary field. Doesn`t shown on site.', max_length=256, null=True, verbose_name='Image description')),
                ('image', versatileimagefield.fields.VersatileImageField(height_field='height', upload_to='category_images', verbose_name='Image', width_field='width')),
                ('width', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image widht')),
                ('height', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image height')),
                ('ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, help_text='Select center point for cropped (resized) image', max_length=20, verbose_name='Image point of interest')),
            ],
            options={
                'verbose_name_plural': 'Images for categories',
                'verbose_name': 'Image for categories',
            },
        ),
        migrations.CreateModel(
            name='LogoImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(blank=True, help_text='Just to distinguish one image from another. It isn`t necessary field. Doesn`t shown on site.', max_length=256, null=True, verbose_name='Image description')),
                ('image', versatileimagefield.fields.VersatileImageField(height_field='height', upload_to='logos', verbose_name='Image', width_field='width')),
                ('width', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image widht')),
                ('height', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image height')),
                ('ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, help_text='Select center point for cropped (resized) image', max_length=20, verbose_name='Image point of interest')),
            ],
            options={
                'verbose_name_plural': 'Manufacturers logos',
                'verbose_name': 'Manufacturer logo',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(help_text='Manufacturer title (in english)', max_length=512, verbose_name='Title (en)')),
                ('title_ru', models.CharField(help_text='Manufacturer title (in russian)', max_length=512, verbose_name='Title (ru)')),
                ('url', models.URLField(blank=True, help_text='Link to company site', max_length=1024, null=True, verbose_name='Site url')),
                ('desc', models.TextField(blank=True, help_text='Company description (4096 symbols max)', max_length=4096, null=True, verbose_name='About')),
                ('contacts', models.TextField(blank=True, help_text='Contacts information', max_length=2048, null=True, verbose_name='Contacts')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Don`t show this entry on site')),
            ],
            options={
                'verbose_name_plural': 'Manufacturers',
                'verbose_name': 'Manufacturer',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(default='', help_text='Product title (in english)', max_length=1024, verbose_name='Title (en)')),
                ('title_ru', models.CharField(default='', help_text='Product title (in russian)', max_length=1024, verbose_name='Title (ru)')),
                ('slug', models.SlugField(default='', help_text='URL representation (a..z, 0..9 and "-" symbols only)', max_length=1024, unique=True, verbose_name='Slug')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Don`t show in catalog')),
                ('desc_short_en', ckeditor.fields.RichTextField(blank=True, default='', help_text='Short device description in english (4096 symbols max)', max_length=4096, null=True, verbose_name='Short description (en)')),
                ('desc_full_en', ckeditor.fields.RichTextField(blank=True, default='', help_text='Full device description in english (10240 symbols max)', max_length=10240, null=True, verbose_name='Full description (en)')),
                ('desc_short_ru', ckeditor.fields.RichTextField(blank=True, default='', help_text='Short device description in russian (4096 symbols max)', max_length=4096, null=True, verbose_name='Short description (ru)')),
                ('desc_full_ru', ckeditor.fields.RichTextField(blank=True, default='', help_text='Full device description in russian (10240 symbols max)', max_length=10240, null=True, verbose_name='Full description (ru)')),
                ('specifications_en', ckeditor.fields.RichTextField(blank=True, default='', help_text='Technical characteristics in english (10240 symbols max)', max_length=10240, null=True, verbose_name='Specifications (en)')),
                ('specifications_ru', ckeditor.fields.RichTextField(blank=True, default='', help_text='Technical characteristics in russian (10240 symbols max)', max_length=10240, null=True, verbose_name='Specifications (ru)')),
                ('options_en', ckeditor.fields.RichTextField(blank=True, default='', help_text='Delivery options in english (4096 symbols max)', max_length=4096, null=True, verbose_name='Options (en)')),
                ('options_ru', ckeditor.fields.RichTextField(blank=True, default='', help_text='Delivery options in russian (4096 symbols max)', max_length=4096, null=True, verbose_name='Options (ru)')),
                ('mentions_en', ckeditor.fields.RichTextField(blank=True, default='', help_text='Links to researches using this device in english (4096 symbols max)', max_length=4096, null=True, verbose_name='Mentions (en)')),
                ('mentions_ru', ckeditor.fields.RichTextField(blank=True, default='', help_text='Links to researches using this device in russian (4096 symbols max)', max_length=4096, null=True, verbose_name='Mentions (ru)')),
                ('categories', models.ManyToManyField(help_text='Subcategories containing this product', to='app.Category')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app.Manufacturer')),
            ],
            options={
                'verbose_name_plural': 'Products',
                'verbose_name': 'Product',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(blank=True, help_text='Just to distinguish one image from another. It isn`t necessary field. Doesn`t shown on site.', max_length=256, null=True, verbose_name='Image description')),
                ('image', versatileimagefield.fields.VersatileImageField(height_field='height', upload_to='product_images', verbose_name='Image', width_field='width')),
                ('width', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image widht')),
                ('height', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image height')),
                ('ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, help_text='Select center point for cropped (resized) image', max_length=20, verbose_name='Image point of interest')),
                ('is_default', models.BooleanField(default=False, help_text='If checked, this image will be set as default in product description. You can chose only one image as default for product.', verbose_name='Is default product image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='app.Product')),
            ],
            options={
                'verbose_name_plural': 'Images for product',
                'verbose_name': 'Image for product',
            },
        ),
        migrations.CreateModel(
            name='TopCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(help_text='Top category title (in english).', max_length=254, verbose_name='Title (en)')),
                ('title_ru', models.CharField(help_text='Top category title (in russian).', max_length=254, verbose_name='Title (ru)')),
                ('slug', models.SlugField(help_text='URL representation (a..z, 0..9 and "-" symbols only)', max_length=254, unique=True, verbose_name='Slug')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Don`t show this entry on site')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='app.CategoryImage')),
            ],
            options={
                'verbose_name_plural': 'Top-level product categories',
                'verbose_name': 'Top-level product category',
            },
        ),
        migrations.AddField(
            model_name='logoimage',
            name='manufacturer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logo', to='app.Manufacturer'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(help_text='Parent top-level category', on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='app.TopCategory'),
        ),
        migrations.AddField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(blank=True, help_text='Products from this category', to='app.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='productimage',
            unique_together=set([('id', 'is_default')]),
        ),
    ]
