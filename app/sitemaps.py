from django.contrib.sitemaps import Sitemap
from app import models
from django.urls import reverse
from django.contrib.sites.models import Site


class StaticViewsMap(Sitemap):
    i18n = True

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='vivariy.com', name='vivariy.com')
        return super(StaticViewsMap, self).get_urls(site=site, **kwargs)

    def items(self):
        return 'main', 'catalog', 'article_list', 'contacts', 'partners',

    def location(self, obj):
        return reverse(obj)


class CatalogSitemap(Sitemap):
    def get_urls(self, site=None, **kwargs):
        site = Site(domain='vivariy.com', name='vivariy.com')
        return super(CatalogSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return models.TopCategory.objects.filter(is_hidden=False)

    def location(self, obj):
        return '/catalog/{}'.format(obj.slug)


class ProductsSitemap(Sitemap):
    def get_urls(self, site=None, **kwargs):
        site = Site(domain='vivariy.com', name='vivariy.com')
        return super(ProductsSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return models.Product.objects.filter(is_hidden=False)

    def location(self, obj):
        return '/products/{}'.format(obj.slug)


class ArticlesSitemap(Sitemap):
    def get_urls(self, site=None, **kwargs):
        site = Site(domain='vivariy.com', name='vivariy.com')
        return super(ArticlesSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return models.Article.objects.filter(is_hidden=False)

    def location(self, obj):
        return '/articles/{}'.format(obj.slug)
