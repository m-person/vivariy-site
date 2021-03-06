# coding=utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from app.models import (Category, TopCategory, Product, Partner, ProductImage, CategoryImage, DocFile, YoutubeVideo,
                        Article, ArticleImage, UserRequest, Employee, CarouselItem, Subscriber, AnalyticsCounter, )


class ProductImageAdmin(admin.ModelAdmin):
    fields = ('desc', 'image', 'product', 'is_default',)
    list_display = ('desc', 'product',)
    save_on_top = True
    change_list_template = 'smuggler/change_list.html'


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = True


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 2
    fields = (('desc', 'is_default'), 'image')


class DocFileInline(admin.StackedInline):
    model = DocFile
    extra = 1
    fields = ('title_ru', 'file', ('product', 'is_hidden'),)


class YoutubeVideoInline(admin.StackedInline):
    model = YoutubeVideo
    extra = 1
    fields = ('title_ru', 'video', ('product', 'is_hidden',),)


class TopCategoryAdmin(admin.ModelAdmin):
    fields = ('title_ru', 'slug', 'image', 'is_hidden')
    list_display = ('title_ru',)
    prepopulated_fields = {
        'slug': ('title_ru',)
    }
    save_on_top = True
    change_list_template = 'smuggler/change_list.html'


class ArticleAdmin(admin.ModelAdmin):
    fields = ('title_ru', 'slug', 'date', 'image', 'source_url', 'cut_ru', 'text_ru', 'tags', 'is_hidden')
    list_display = ('title_ru',)
    prepopulated_fields = {
        'slug': ('title_ru',)
    }
    save_on_top = True
    change_list_template = 'smuggler/change_list.html'


class CategoryAdmin(admin.ModelAdmin):
    fields = ('title_ru', 'parent_category', 'products', 'is_hidden')
    # list_display = ('title_ru', 'parent_category')
    list_display = ('title_ru',)
    save_on_top = True
    change_list_template = 'smuggler/change_list.html'


class PartnerAdmin(admin.ModelAdmin):
    fields = (('title', 'title_en',), 'desc', 'desc_en', 'image', 'is_hidden')
    list_display = ('title',)
    prepopulated_fields = {
        'title_en': ('title',)
    }
    save_on_top = True
    change_list_template = 'smuggler/change_list.html'


class ProductAdmin(admin.ModelAdmin):
    fields = ('title_ru', 'slug', 'manufacturer', 'categories', 'desc_short_ru', 'desc_full_ru', 'specifications_ru',
              'options_ru', 'mentions_ru', 'faq_ru', 'is_hidden')
    list_display = ('title_ru', 'manufacturer')
    prepopulated_fields = {
        'slug': ('title_ru',)
    }
    inlines = (ProductImageInline, DocFileInline, YoutubeVideoInline,)
    save_on_top = True
    change_list_template = 'smuggler/change_list.html'


class CategoryImageAdmin(admin.ModelAdmin):
    fields = ('desc', 'image',)
    list_display = ('desc',)
    save_on_top = True
    change_list_template = 'smuggler/change_list.html'


class ArticleImageAdmin(admin.ModelAdmin):
    fields = ('desc', 'image',)
    list_display = ('desc',)
    save_on_top = True
    change_list_template = 'smuggler/change_list.html'


class DocFileAdmin(admin.ModelAdmin):
    fields = ('title_ru', 'file', 'product', 'is_hidden')
    list_display = ('title_ru',)
    save_on_top = True
    change_list_template = 'smuggler/change_list.html'


class YoutubeVideoAdmin(admin.ModelAdmin):
    fields = ('title_ru', 'video', 'product', 'is_hidden')
    list_display = ('title_ru',)
    save_on_top = True
    change_list_template = 'smuggler/change_list.html'


class UserRequestAdmin(admin.ModelAdmin):
    readonly_fields = (
        'org_title', 'name', 'email', 'phone', 'cart', 'message', 'timestamp', 'email_is_sent', 'error_message',)
    list_display = ('timestamp', 'name', 'email', 'email_is_sent',)
    save_on_top = True
    change_list_template = 'smuggler/change_list.html'


class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)
    change_list_template = 'smuggler/change_list.html'


class CarouselItemAdmin(admin.ModelAdmin):
    fields = ('title', 'order_position', 'desc', 'url', 'image', 'is_hidden')
    list_display = ('title', 'order_position',)
    save_on_top = True
    change_list_template = 'smuggler/change_list.html'


class SubscriberAdmin(admin.ModelAdmin):
    fields = ('email', 'is_active', 'timestamp')
    readonly_fields = ('email', 'timestamp')
    save_on_top = True
    list_display = ('email', 'is_active', 'timestamp')
    change_list_template = 'smuggler/change_list.html'


class AnalyticsCounterAdmin(admin.ModelAdmin):
    fields = ('name', 'is_enabled', 'code')
    save_on_top = True
    list_display = ('name', 'is_enabled')


admin.site.register(CarouselItem, CarouselItemAdmin)
admin.site.register(CategoryImage, CategoryImageAdmin)
admin.site.register(TopCategory, TopCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(DocFile, DocFileAdmin)
admin.site.register(YoutubeVideo, YoutubeVideoAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleImage, ArticleImageAdmin)
admin.site.register(UserRequest, UserRequestAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(AnalyticsCounter, AnalyticsCounterAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
