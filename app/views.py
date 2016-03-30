# coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, RedirectView
from app.models import (Category, Product, TopCategory, Manufacturer, Article)
from django.core.urlresolvers import reverse


class MainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        ctx = super(MainView, self).get_context_data(**kwargs)
        ctx['menuitem'] = 'main'
        ctx['top_categories'] = TopCategory.objects.filter(is_hidden=False)
        ctx['articles'] = Article.objects.filter(is_hidden=False).order_by('-date')[:3]
        return ctx


class CatalogViewRedirect(RedirectView):
    permanent = False
    pattern_name = 'category'

    def get_redirect_url(self, *args, **kwargs):
        kwargs['slug'] = TopCategory.objects.all()[0]
        return reverse('category', kwargs=kwargs)


class CatalogView(TemplateView):
    template_name = 'catalog.html'

    def get_context_data(self, **kwargs):
        ctx = super(CatalogView, self).get_context_data(**kwargs)
        ctx['menuitem'] = 'catalog'
        ctx['top_categories'] = TopCategory.objects.filter(is_hidden=False)
        return ctx


class CategoryView(TemplateView):
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        ctx = super(CategoryView, self).get_context_data(**kwargs)
        ctx['menuitem'] = 'catalog'
        parent = get_object_or_404(TopCategory, slug=kwargs['slug'])
        ctx['current_top_category'] = parent
        ctx['top_categories'] = TopCategory.objects.filter(is_hidden=False)
        ctx['categories'] = Category.objects.filter(is_hidden=False, parent_category=parent)
        return ctx


class ProductView(TemplateView):
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        ctx = super(ProductView, self).get_context_data(**kwargs)
        ctx['menuitem'] = 'catalog'
        product = get_object_or_404(Product, slug=kwargs['slug'])
        ctx['top_category'] = product.categories.all()[0].parent_category
        ctx['docfiles'] = product.doc_files.filter(is_hidden=False)
        ctx['videos'] = product.videos.filter(is_hidden=False)
        ctx['product'] = product
        return ctx


class ManufacturersView(TemplateView):
    template_name = 'manufacturers.html'

    def get_context_data(self, **kwargs):
        ctx = super(ManufacturersView, self).get_context_data(**kwargs)
        ctx['menuitem'] = 'partners'
        ctx['partner_list'] = Manufacturer.objects.filter(is_hidden=False)
        return ctx


class ArticleListView(TemplateView):
    template_name = 'article-list.html'

    def get_context_data(self, **kwargs):
        ctx = super(ArticleListView, self).get_context_data(**kwargs)
        ctx['menuitem'] = 'articles'
        ctx['articles'] = Article.objects.filter(is_hidden=False)  # todo: add pagination
        return ctx


class ArticleDetailView(TemplateView):
    template_name = 'article-details.html'

    def get_context_data(self, **kwargs):
        ctx = super(ArticleDetailView, self).get_context_data(**kwargs)
        ctx['menuitem'] = 'articles'
        ctx['article'] = get_object_or_404(Article, slug=kwargs['slug'])
        return ctx
