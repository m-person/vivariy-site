from django.contrib.sitemaps import Sitemap
from app import models
from django.core.urlresolvers import reverse


class StaticViewsMap(Sitemap):
    i18n = True

    def items(self):
        return 'main', 'catalog', 'article_list', 'contacts', 'partners',

    def location(self, obj):
        return reverse(obj)


class CatalogSitemap(Sitemap):
    def items(self):
        return models.TopCategory.objects.filter(is_hidden=False)

    def location(self, obj):
        return '/catalog/{}'.format(obj.slug)


class ProductsSitemap(Sitemap):
    def items(self):
        return models.Product.objects.filter(is_hidden=False)

    def location(self, obj):
        return '/products/{}'.format(obj.slug)


class ArticlesSitemap(Sitemap):
    def items(self):
        return models.Article.objects.filter(is_hidden=False)

    def location(self, obj):
        return '/articles/{}'.format(obj.slug)
