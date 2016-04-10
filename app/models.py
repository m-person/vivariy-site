# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from ckeditor.fields import RichTextField
from versatileimagefield.fields import (VersatileImageField, PPOIField, )
from tagging_autocomplete.models import TagAutocompleteField
from django.contrib.auth.models import User


class ArticleImage(models.Model):
    """
    Image to describe article.
    """
    desc = models.CharField(_('Image description'), blank=True, null=True, max_length=256,
                            help_text=_('Just to distinguish one image from another. It isn`t necessary field.'
                                        ' Doesn`t shown on site.'))
    image = VersatileImageField(_('Image'), upload_to='article_images', width_field='width', height_field='height',
                                ppoi_field='ppoi')
    width = models.PositiveIntegerField(_('Image widht'), blank=True, null=True)
    height = models.PositiveIntegerField(_('Image height'), blank=True, null=True)
    ppoi = PPOIField(_('Image point of interest'), help_text=_('Select center point for cropped (resized) image'))

    def __str__(self):
        return self.desc

    class Meta:
        verbose_name = _('Image for articles')
        verbose_name_plural = _('Images for articles')


class CategoryImage(models.Model):
    """
    Images for product categories
    """
    desc = models.CharField(_('Image description'), blank=True, null=True, max_length=256,
                            help_text=_('Just to distinguish one image from another. It isn`t necessary field.'
                                        ' Doesn`t shown on site.'))
    image = VersatileImageField(_('Image'), upload_to='category_images', width_field='width', height_field='height',
                                ppoi_field='ppoi')
    width = models.PositiveIntegerField(_('Image widht'), blank=True, null=True)
    height = models.PositiveIntegerField(_('Image height'), blank=True, null=True)
    ppoi = PPOIField(_('Image point of interest'), help_text=_('Select center point for cropped (resized) image'))

    def __str__(self):
        return self.desc

    class Meta:
        verbose_name = _('Image for categories')
        verbose_name_plural = _('Images for categories')


class ProductImage(models.Model):
    """
    Images for product
    """
    desc = models.CharField(_('Image description'), blank=True, null=True, max_length=256,
                            help_text=_('Just to distinguish one image from another. It isn`t necessary field.'
                                        ' Doesn`t shown on site.'))
    image = VersatileImageField(_('Image'), upload_to='product_images', width_field='width', height_field='height',
                                ppoi_field='ppoi')
    width = models.PositiveIntegerField(_('Image widht'), blank=True, null=True)
    height = models.PositiveIntegerField(_('Image height'), blank=True, null=True)
    ppoi = PPOIField(_('Image point of interest'), help_text=_('Select center point for cropped (resized) image'))
    product = models.ForeignKey('Product', related_name='images')
    is_default = models.BooleanField(_('Is default product image'), default=False,
                                     help_text=_('If checked, this image will be set as default in product description.'
                                                 ' You can chose only one image as default for product.'))

    def __str__(self):
        return self.desc

    class Meta:
        verbose_name = _('Image for product')
        verbose_name_plural = _('Images for product')
        unique_together = (('id', 'is_default',),)


class TopCategory(models.Model):
    """
    Top-level category. It's just a parent for subcategories.
    """
    title_ru = models.CharField(_('Title (ru)'), max_length=254, help_text=_('Top category title (in russian).'))
    slug = models.SlugField(_('Slug'), max_length=254, unique=True, db_index=True,
                            help_text=_('URL representation (a..z, 0..9 and "-" symbols only)'))
    image = models.ForeignKey('CategoryImage', related_name='categories')
    is_hidden = models.BooleanField(_('Don`t show this entry on site'), default=False)

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = _('Top-level product category')
        verbose_name_plural = _('Top-level product categories')


class Category(models.Model):
    """
    Product category (second level, container for products).
    """
    title_ru = models.CharField(_('Title (ru)'), max_length=254, help_text=_('Category title (in russian).'))
    is_hidden = models.BooleanField(_('Don`t show this entry on site'), default=False)
    parent_category = models.ManyToManyField('TopCategory', related_name='categories',
                                             help_text=_('Parent top-level categories'))
    products = models.ManyToManyField('Product', blank=True, help_text=_('Products from this category'))

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = _('Product category')
        verbose_name_plural = _('Product categories')


class Partner(models.Model):
    """
    Partner company
    """
    title = models.CharField(_('Name'), max_length=512, help_text=_('Company`s name'))
    desc = models.TextField(_('Description'), max_length=4096, blank=True, null=True,
                            help_text=_('Company description (4096 symbols max)'))
    is_hidden = models.BooleanField(_('Don`t show this entry on site'), default=False)
    image = VersatileImageField(_('Image'), upload_to='partners', blank=True, null=True,
                                width_field='width', height_field='height', ppoi_field='ppoi')
    width = models.PositiveIntegerField(_('Image widht'), blank=True, null=True)
    height = models.PositiveIntegerField(_('Image height'), blank=True, null=True)
    ppoi = PPOIField(_('Image point of interest'), help_text=_('Select center point for cropped (resized) image'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Partner')
        verbose_name_plural = _('Partners')


class Product(models.Model):
    """
    Product item
    """
    title_ru = models.CharField(_('Title (ru)'), max_length=1024, default='', help_text=_('Product title (in russian)'))
    slug = models.SlugField(_('Slug'), max_length=1024, unique=True, default='', db_index=True,
                            help_text=_('URL representation (a..z, 0..9 and "-" symbols only)'))
    manufacturer = models.ForeignKey('Partner', related_name='products', blank=True, null=True)
    is_hidden = models.BooleanField(_('Don`t show in catalog'), default=False)
    categories = models.ManyToManyField('Category', help_text=_('Subcategories containing this product'))
    desc_short_ru = RichTextField(_('Short description (ru)'), max_length=4096, default='', blank=True, null=True,
                                  help_text=_('Short device description in russian (4096 symbols max)'))
    desc_full_ru = RichTextField(_('Full description (ru)'), max_length=10240, default='', blank=True, null=True,
                                 help_text=_('Full device description in russian (10240 symbols max)'))
    specifications_ru = RichTextField(_('Specifications (ru)'), max_length=10240, default='', blank=True, null=True,
                                      help_text=_('Technical characteristics in russian (10240 symbols max)'))
    options_ru = RichTextField(_('Options (ru)'), max_length=4096, default='', blank=True, null=True,
                               help_text=_('Delivery options in russian (4096 symbols max)'))
    mentions_ru = RichTextField(_('Mentions (ru)'), max_length=4096, default='', blank=True, null=True,
                                help_text=_('Links to researches using this device in russian (4096 symbols max)'))

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class DocFile(models.Model):
    """
    File with additional information for product. For downloads.
    """
    title_ru = models.CharField(_('Title (ru)'), max_length=128, help_text=_('File title (in russian)'))
    product = models.ForeignKey(Product, related_name='doc_files')
    is_hidden = models.BooleanField(_('Don`t show it on site'), default=False)
    file = models.FileField(_('File'), upload_to='doc_files/')

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = _('Doc file')
        verbose_name_plural = _('Doc files')


class YoutubeVideo(models.Model):
    """
    Embedded youtube video for product
    """
    title_ru = models.CharField(_('Title (ru)'), max_length=128, help_text=_('Video title (in russian)'))
    product = models.ForeignKey(Product, related_name='videos')
    is_hidden = models.BooleanField(_('Don`t show it on site'), default=False)
    video = models.CharField(_('Embedding code'), max_length=1024,
                             help_text=_('Video embedding code from youtube.com. To obtain it, choose "share" > "embed"'
                                         ' on youtube page with video.'))

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = _('Youtube video')
        verbose_name_plural = _('Youtube videos')


class Article(models.Model):
    """
    An article (news item).
    """
    title_ru = models.CharField(_('Title (ru)'), max_length=512, help_text=_('Article title (in russian)'))
    slug = models.SlugField(_('Slug'), max_length=254, unique=True, db_index=True,
                            help_text=_('URL representation (a..z, 0..9 and "-" symbols only)'))
    cut_ru = models.CharField(_('Cut text (ru)'), default='', max_length=4096,
                              help_text=_('Truncated article (in russian)'))
    text_ru = RichTextField(_('Article text (ru)'), default='', null=True,
                            help_text=(_('Full article text (in russian)')))
    date = models.DateTimeField(_('Date'), default=timezone.now, help_text=_('Article creation date'))
    is_hidden = models.BooleanField(_('Don`t show it on site'), default=False)
    source_url = models.URLField(_('Link to source'), max_length=1024, help_text=_('Source url'))
    image = models.ForeignKey('ArticleImage', related_name='articles')
    tags = TagAutocompleteField(_('Artilcle tags'), help_text=_('Add list of article tags separated by commas'))

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')


class UserRequest(models.Model):
    """
    User request for additional info
    """
    org_title = models.CharField(_('Organization title'), max_length=512, blank=True, null=True)
    name = models.CharField(_('Your name*'), max_length=512)
    email = models.EmailField(_('Your contact e-mail*'))
    phone = models.CharField(_('Your contact phone*'), max_length=128)
    message = models.TextField(_('Additional information'), max_length=4096, blank=True, null=True)
    timestamp = models.DateTimeField(_('Message time'), auto_now_add=True)
    cart = models.CharField(_('List of products to ask'), max_length=4096, default='')

    def __str__(self):
        return "{} ({})".format(self.name, self.email, )


class Employee(models.Model):
    """
    extend default user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_mail_recipient = models.BooleanField(_('Receive requests mail?'), default=False, help_text=_(
        'Check it if this user will receive emails with customer requests.'))

    def __str__(self):
        return self.user.username


class CarouselItem(models.Model):
    """
    slide content for carousel on main page
    """
    title = models.CharField(_('Title'), max_length=128, help_text=_('Slide header'))
    desc = models.TextField(_('Description'), max_length=512, help_text=_('Description text'))
    url = models.URLField(_('URL'), max_length=1024, help_text=_('Links to details page.'))
    is_hidden = models.BooleanField(_('Hide this slide'), default=False)
    image = VersatileImageField(_('Image'), upload_to='slides', width_field='width', height_field='height',
                                ppoi_field='ppoi')
    width = models.PositiveIntegerField(_('Image widht'), blank=True, null=True)
    height = models.PositiveIntegerField(_('Image height'), blank=True, null=True)
    ppoi = PPOIField(_('Image point of interest'), help_text=_('Select center point for cropped (resized) image'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Slide')
        verbose_name_plural = _('Slides')
