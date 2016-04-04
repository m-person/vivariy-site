# coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, RedirectView, View
from django.views.generic.edit import BaseUpdateView
from app.models import (Category, Product, TopCategory, Manufacturer, Article)
from django.core.urlresolvers import reverse
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from tagging.models import Tag, TaggedItem
from django.http import JsonResponse


class MyPaginator(Paginator):
    """
    Purpose: just to avoid too many "if" tags in template.
    """

    def shortened_page_range(self, count=3):
        """
        shortens too long list of pages: replaces excess elements in middle of the list by "..."
        for example: list [1,2,3,4,5,6,7,8,9] with count=3 will be converted to [1,2,3,"...",9]
        :param count: how many first items don't skip
        """
        page_range = list(self.page_range)
        if len(page_range) <= count + 2:
            return page_range
        return page_range[:count] + ['...'] + page_range[-1:]


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

    def post(self, request, *args, **kwargs):
        # add product to cart (list of products for future request)
        item = kwargs.get('slug')
        if item:
            if not 'cart' in request.session.keys():
                request.session['cart'] = {}
            request.session['cart'][item] = None
        return JsonResponse({'result': 'ok'})

    def delete(self, request, *args, **kwargs):
        # remove product form cart (list of products for mail request)
        item = kwargs.get('slug')
        if item and 'cart' in request.session.keys():
            request.session['cart'].pop(item)
            return JsonResponse({'result': 'ok'})
        return JsonResponse({'result': 'error'})


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
        items_on_page = 2  # todo: change it after debug
        ctx = super(ArticleListView, self).get_context_data(**kwargs)
        ctx['menuitem'] = 'articles'
        ctx['tags'] = Tag.objects.all()

        page = self.request.GET.get('page')
        tag = self.request.GET.get('filter')

        # construct url, otherwise it'll too much logic in template considering filtering by tag and pagination
        if tag:
            ctx['current_url'] = '/articles/?filter=' + tag + '&'
            ctx['current_tag'] = tag
        else:
            ctx['current_url'] = '/articles/?'

        if tag:
            try:
                curr_tag = Tag.objects.get(name=tag)
                paginator = MyPaginator(TaggedItem.objects.get_by_model(Article, curr_tag).filter(is_hidden=False),
                                        items_on_page)
            except Tag.DoesNotExist:
                paginator = MyPaginator(Article.objects.filter(is_hidden=False), items_on_page)
        else:
            paginator = MyPaginator(Article.objects.filter(is_hidden=False), items_on_page)

        try:
            ctx['articles'] = paginator.page(page)
        except PageNotAnInteger:
            ctx['articles'] = paginator.page(1)
        except EmptyPage:
            ctx['articles'] = paginator.page(paginator.num_pages)
        return ctx


class ArticleDetailView(TemplateView):
    template_name = 'article-details.html'

    def get_context_data(self, **kwargs):
        ctx = super(ArticleDetailView, self).get_context_data(**kwargs)
        ctx['menuitem'] = 'articles'
        ctx['article'] = get_object_or_404(Article, slug=kwargs['slug'])
        return ctx


class ContactsView(TemplateView):
    template_name = 'contacts.html'

    def get_context_data(self, **kwargs):
        ctx = super(ContactsView, self).get_context_data(**kwargs)
        ctx['menuitem'] = 'contacts'

        # get from session product items for request
        ctx['product'] = Product.objects.all()[0]  # todo: just for autocomplete in template. delete it.
        if self.request.session['cart']:
            ctx['cart'] = []
            for product_slug in self.request.session['cart'].keys():
                try:
                    ctx['cart'].append(Product.objects.get(slug=product_slug))
                except Product.DoesNotExist:
                    pass
        return ctx
