# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-07 15:37
from __future__ import unicode_literals

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tagging_autocomplete.models
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_ru', models.CharField(help_text='Article title (in russian)', max_length=512, verbose_name='Title (ru)')),
                ('slug', models.SlugField(help_text='URL representation (a..z, 0..9 and "-" symbols only)', max_length=254, unique=True, verbose_name='Slug')),
                ('cut_ru', models.CharField(default='', help_text='Truncated article (in russian)', max_length=4096, verbose_name='Cut text (ru)')),
                ('text_ru', ckeditor.fields.RichTextField(default='', help_text='Full article text (in russian)', null=True, verbose_name='Article text (ru)')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, help_text='Article creation date', verbose_name='Date')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Don`t show it on site')),
                ('source_url', models.URLField(help_text='Source url', max_length=1024, verbose_name='Link to source')),
                ('tags', tagging_autocomplete.models.TagAutocompleteField(blank=True, help_text='Add list of article tags separated by commas', max_length=255, verbose_name='Artilcle tags')),
            ],
            options={
                'verbose_name_plural': 'Articles',
                'verbose_name': 'Article',
            },
        ),
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(blank=True, help_text='Just to distinguish one image from another. It isn`t necessary field. Doesn`t shown on site.', max_length=256, null=True, verbose_name='Image description')),
                ('image', versatileimagefield.fields.VersatileImageField(height_field='height', upload_to='article_images', verbose_name='Image', width_field='width')),
                ('width', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image widht')),
                ('height', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image height')),
                ('ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, help_text='Select center point for cropped (resized) image', max_length=20, verbose_name='Image point of interest')),
            ],
            options={
                'verbose_name_plural': 'Images for articles',
                'verbose_name': 'Image for articles',
            },
        ),
        migrations.CreateModel(
            name='CarouselItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Slide header', max_length=128, verbose_name='Title')),
                ('desc', models.TextField(help_text='Description text', max_length=512, verbose_name='Description')),
                ('url', models.URLField(help_text='Links to details page.', max_length=1024, verbose_name='URL')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Hide this slide')),
                ('image', versatileimagefield.fields.VersatileImageField(height_field='height', upload_to='slides', verbose_name='Image', width_field='width')),
                ('width', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image widht')),
                ('height', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image height')),
                ('ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, help_text='Select center point for cropped (resized) image', max_length=20, verbose_name='Image point of interest')),
            ],
            options={
                'verbose_name_plural': 'Slides',
                'verbose_name': 'Slide',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
            name='DocFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_ru', models.CharField(help_text='File title (in russian)', max_length=128, verbose_name='Title (ru)')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Don`t show it on site')),
                ('file', models.FileField(upload_to='doc_files/', verbose_name='File')),
            ],
            options={
                'verbose_name_plural': 'Doc files',
                'verbose_name': 'Doc file',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_mail_recipient', models.BooleanField(default=False, help_text='Check it if this user will receive emails with customer requests.', verbose_name='Receive requests mail?')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Company`s name', max_length=512, verbose_name='Name')),
                ('desc', models.TextField(blank=True, help_text='Company description (4096 symbols max)', max_length=4096, null=True, verbose_name='Description')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Don`t show this entry on site')),
                ('image', versatileimagefield.fields.VersatileImageField(blank=True, height_field='height', null=True, upload_to='partners', verbose_name='Image', width_field='width')),
                ('width', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image widht')),
                ('height', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image height')),
                ('ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, help_text='Select center point for cropped (resized) image', max_length=20, verbose_name='Image point of interest')),
            ],
            options={
                'verbose_name_plural': 'Partners',
                'verbose_name': 'Partner',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_ru', models.CharField(default='', help_text='Product title (in russian)', max_length=1024, verbose_name='Title (ru)')),
                ('slug', models.SlugField(default='', help_text='URL representation (a..z, 0..9 and "-" symbols only)', max_length=1024, unique=True, verbose_name='Slug')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Don`t show in catalog')),
                ('desc_short_ru', ckeditor.fields.RichTextField(blank=True, default='', help_text='Short device description in russian (4096 symbols max)', max_length=4096, null=True, verbose_name='Short description (ru)')),
                ('desc_full_ru', ckeditor.fields.RichTextField(blank=True, default='', help_text='Full device description in russian (10240 symbols max)', max_length=10240, null=True, verbose_name='Full description (ru)')),
                ('specifications_ru', ckeditor.fields.RichTextField(blank=True, default='', help_text='Technical characteristics in russian (10240 symbols max)', max_length=10240, null=True, verbose_name='Specifications (ru)')),
                ('options_ru', ckeditor.fields.RichTextField(blank=True, default='', help_text='Delivery options in russian (4096 symbols max)', max_length=4096, null=True, verbose_name='Options (ru)')),
                ('mentions_ru', ckeditor.fields.RichTextField(blank=True, default='', help_text='Links to researches using this device in russian (4096 symbols max)', max_length=4096, null=True, verbose_name='Mentions (ru)')),
                ('categories', models.ManyToManyField(help_text='Subcategories containing this product', to='app.Category')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app.Partner')),
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
        migrations.CreateModel(
            name='UserRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_title', models.CharField(blank=True, max_length=512, null=True, verbose_name='Organization title')),
                ('name', models.CharField(max_length=512, verbose_name='Your name*')),
                ('email', models.EmailField(max_length=254, verbose_name='Your contact e-mail*')),
                ('phone', models.CharField(max_length=128, verbose_name='Your contact phone*')),
                ('message', models.TextField(blank=True, max_length=4096, null=True, verbose_name='Additional information')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Message time')),
                ('cart', models.CharField(default='', max_length=4096, verbose_name='List of products to ask')),
            ],
        ),
        migrations.CreateModel(
            name='YoutubeVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_ru', models.CharField(help_text='Video title (in russian)', max_length=128, verbose_name='Title (ru)')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Don`t show it on site')),
                ('video', models.CharField(help_text='Video embedding code from youtube.com. To obtain it, choose "share" > "embed" on youtube page with video.', max_length=1024, verbose_name='Embedding code')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='app.Product')),
            ],
            options={
                'verbose_name_plural': 'Youtube videos',
                'verbose_name': 'Youtube video',
            },
        ),
        migrations.AddField(
            model_name='docfile',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doc_files', to='app.Product'),
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
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='app.ArticleImage'),
        ),
        migrations.AlterUniqueTogether(
            name='productimage',
            unique_together=set([('id', 'is_default')]),
        ),
    ]
