# coding=utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from app.models import (Category, TopCategory, Product, Manufacturer, ProductImage, CategoryImage, LogoImage,
                        DocFile, YoutubeVideo, Article, ArticleImage, UserRequest, Employee, )


class ProductImageAdmin(admin.ModelAdmin):
    fields = ('desc', 'image', 'product', 'is_default',)
    list_display = ('desc', 'product',)
    save_on_top = True


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = True


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 2
    fields = (('desc', 'is_default'), 'image')


class LogoImageInline(admin.StackedInline):
    model = LogoImage
    extra = 1
    fields = (('desc', 'image',),)


class DocFileInline(admin.StackedInline):
    model = DocFile
    extra = 1
    fields = (('title_ru', 'title_en'), 'file', ('product', 'is_hidden'),)


class YoutubeVideoInline(admin.StackedInline):
    model = YoutubeVideo
    extra = 1
    fields = (('title_ru', 'title_en'), 'video', ('product', 'is_hidden',),)


class TopCategoryAdmin(admin.ModelAdmin):
    fields = ('title_ru', 'title_en', 'slug', 'image', 'is_hidden')
    list_display = ('title_ru',)
    prepopulated_fields = {
        'slug': ('title_en',)
    }
    save_on_top = True


class ArticleAdmin(admin.ModelAdmin):
    fields = (
        ('title_ru', 'title_en',), 'slug', 'date', 'image', 'source_url', ('cut_ru', 'cut_en',),
        ('text_en', 'text_ru',), 'tags', 'is_hidden')
    list_display = ('title_ru',)
    prepopulated_fields = {
        'slug': ('title_en',)
    }
    save_on_top = True


class CategoryAdmin(admin.ModelAdmin):
    fields = ('title_ru', 'title_en', 'parent_category', 'products', 'is_hidden')
    list_display = ('title_ru', 'parent_category')
    save_on_top = True


class ManufacturerAdmin(admin.ModelAdmin):
    fields = (('title_ru', 'title_en'), 'desc', 'contacts', 'url', 'is_hidden')
    list_display = ('title_ru',)
    inlines = (LogoImageInline,)
    save_on_top = True


class ProductAdmin(admin.ModelAdmin):
    fields = (('title_ru', 'title_en'), 'slug', 'manufacturer', 'categories', ('desc_short_ru', 'desc_short_en'),
              ('desc_full_ru', 'desc_full_en'), ('specifications_ru', 'specifications_en'),
              ('options_ru', 'options_en'), ('mentions_ru', 'mentions_en'), 'is_hidden')
    list_display = ('title_ru', 'manufacturer')
    prepopulated_fields = {
        'slug': ('title_en',)
    }
    inlines = (ProductImageInline, DocFileInline, YoutubeVideoInline,)
    save_on_top = True


class CategoryImageAdmin(admin.ModelAdmin):
    fields = ('desc', 'image',)
    list_display = ('desc',)
    save_on_top = True


class ArticleImageAdmin(admin.ModelAdmin):
    fields = ('desc', 'image',)
    list_display = ('desc',)
    save_on_top = True


class DocFileAdmin(admin.ModelAdmin):
    fields = (('title_ru', 'title_en'), 'file', 'product', 'is_hidden')
    list_display = ('title_ru',)
    save_on_top = True


class YoutubeVideoAdmin(admin.ModelAdmin):
    fields = (('title_ru', 'title_en',), 'video', 'product', 'is_hidden')
    list_display = ('title_ru',)
    save_on_top = True


class UserRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('org_title', 'name', 'email', 'phone', 'cart', 'message', 'timestamp')
    list_display = ('timestamp', 'name', 'email',)
    save_on_top = True


class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)


admin.site.register(CategoryImage, CategoryImageAdmin)
admin.site.register(TopCategory, TopCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(DocFile, DocFileAdmin)
admin.site.register(YoutubeVideo, YoutubeVideoAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleImage, ArticleImageAdmin)
admin.site.register(UserRequest, UserRequestAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
