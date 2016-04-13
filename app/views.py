# coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, RedirectView, FormView
from app.models import (Category, Product, TopCategory, Partner, Article, Employee, CarouselItem, )
from django.core.urlresolvers import reverse
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from tagging.models import Tag, TaggedItem
from django.http import JsonResponse
from app.forms import UserRequestForm
import json
from django.core.mail import send_mail
from smtplib import SMTPException
from django.template.loader import render_to_string
from copy import copy
from random import randint


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
        ctx['slides'] = CarouselItem.objects.filter(is_hidden=False)
        ctx['slide_initial'] = randint(0,ctx['slides'].count()-1)
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


class PartnersView(TemplateView):
    template_name = 'partners.html'

    def get_context_data(self, **kwargs):
        ctx = super(PartnersView, self).get_context_data(**kwargs)
        ctx['menuitem'] = 'partners'
        ctx['partner_list'] = Partner.objects.filter(is_hidden=False)
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
        article = get_object_or_404(Article, slug=kwargs['slug'])
        ctx['article'] = article
        ctx['tags'] = Tag.objects.all()
        ctx['article_tags'] = Tag.objects.get_for_object(article)
        return ctx


class RequestSuccess(TemplateView):
    template_name = 'request_success.html'


class ContactsView(FormView):
    template_name = 'contacts.html'
    form_class = UserRequestForm
    success_url = '/request_success/'

    def get_context_data(self, **kwargs):
        ctx = super(ContactsView, self).get_context_data(**kwargs)
        ctx['menuitem'] = 'contacts'

        # get the product items for request from session
        if 'cart' in self.request.session:
            ctx['cart'] = []
            for product_slug in self.request.session['cart'].keys():
                try:
                    ctx['cart'].append(Product.objects.get(slug=product_slug))
                except Product.DoesNotExist:
                    pass
        return ctx

    def form_valid(self, form):
        data = form.cleaned_data
        data.pop('captcha')
        data['cart'] = self.hrefs_from_cart()
        recipients = [empl.user.email for empl in Employee.objects.filter(is_mail_recipient=True)]
        try:
            if send_mail(subject='User request', message=self.email_as_text(data), recipient_list=recipients,
                         from_email=None, html_message=self.email_as_html(data)
                         ):
                self.request.session.pop('cart')
        except SMTPException:
            pass
        # UserRequest.objects.create(**data)
        return super(ContactsView, self).form_valid(form)

    def hrefs_from_cart(self):
        # extracts list of products from cart, and return them as list of http links (in json format)
        if not self.request.session['cart']:
            return '[]'
        host = self.request.get_host()
        return json.dumps(
            ["http://{}/products/{}".format(host, slug, ) for slug in self.request.session['cart'].keys()]
        )

    @staticmethod
    def email_as_html(ctx):
        """
        renders email body in html format
        """
        ctx2 = copy(ctx)  # preserve original context from changing
        if 'cart' in ctx:
            ctx2['products'] = json.loads(ctx['cart'])
        return render_to_string('mail_request.html', context=ctx2)

    @staticmethod
    def email_as_text(ctx):
        """
        renders email body in txt format
        """
        res = ''
        for k, v in ctx.items():
            res += "{}: {}\n".format(k, v)
        return res
