# coding=utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, RedirectView, FormView
from django.core.exceptions import ObjectDoesNotExist
from app.models import (Category, Product, TopCategory, Partner, Article, Employee, CarouselItem, UserRequest,
                        Subscriber, )
from django.core.urlresolvers import reverse
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from tagging.models import Tag, TaggedItem
from django.http import JsonResponse
from app.forms import UserRequestForm, SubscriberForm
import json
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from copy import copy
from random import randint
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from datetime import datetime
import tarfile
import csv


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
        ctx['slides'] = CarouselItem.objects.filter(is_hidden=False).order_by('order_position')
        if ctx['slides'].count() > 0:
            ctx['slide_initial'] = randint(0, ctx['slides'].count() - 1)
        else:
            ctx['slide_initial'] = 0
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
        ctx['top_category'] = product.categories.all()[0].parent_category.all()[0]
        ctx['docfiles'] = product.doc_files.filter(is_hidden=False)
        ctx['videos'] = product.videos.filter(is_hidden=False)
        ctx['product'] = product
        ctx['images'] = self.get_ordered_images(product)
        return ctx

    def post(self, request, *args, **kwargs):
        # add product to cart (list of products for future request)
        if 'delete_method' in request.POST:  # for non-ajax requests
            return self.delete(request, *args, **kwargs)
        item = kwargs.get('slug')
        if item:
            if not 'cart' in request.session.keys():
                request.session['cart'] = {}
            request.session['cart'][item] = None
        if self.request.is_ajax():
            return JsonResponse({'result': 'ok'})
        else:
            return redirect(self.request.path, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # remove product form cart (list of products for mail request)
        item = kwargs.get('slug')
        if item and 'cart' in request.session.keys():
            request.session['cart'].pop(item)
            if request.is_ajax():
                return JsonResponse({'result': 'ok'})
            else:
                return redirect('contacts')
        if request.is_ajax():
            return JsonResponse({'result': 'error'})
        else:
            return redirect('contacts')

    @staticmethod
    def get_ordered_images(product):
        # returns list of product images with default image at first place
        assert isinstance(product, Product)
        res = list(product.images.filter(is_default=False))
        try:
            res.insert(0, product.images.get(is_default=True))
        except ObjectDoesNotExist:
            pass
        return res


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
        items_on_page = 10
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
                paginator = MyPaginator(
                    TaggedItem.objects.get_by_model(Article, curr_tag).filter(is_hidden=False).order_by('-date'),
                    items_on_page)
            except Tag.DoesNotExist:
                paginator = MyPaginator(Article.objects.filter(is_hidden=False).order_by('-date'), items_on_page)
        else:
            paginator = MyPaginator(Article.objects.filter(is_hidden=False).order_by('-date'), items_on_page)

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
        email_is_sent = False
        recipients = [empl.user.email for empl in Employee.objects.filter(is_mail_recipient=True)]
        try:
            if send_mail(subject='Vivariy.com: user request', message=self.email_as_text(data),
                         recipient_list=recipients, from_email=settings.EMAIL_HOST_USER,
                         html_message=self.email_as_html(data)):
                self.request.session.pop('cart')
                data['email_is_sent'] = True
                email_is_sent = True
                send_mail(subject='Vivariy.com: подтверждение запроса',
                          message='Уважаемый {},\nВаш запрос был получен.\n\nВ скором времени с вами свяжется наш сотрудник.\n\n\n\n-------------\nгруппа компаний "Виварий"'.format(
                              data['name']),
                          recipient_list=[data['email']],
                          from_email=settings.EMAIL_HOST_USER)
        except Exception:
            pass
        UserRequest.objects.create(**data)
        return render(self.request, 'request_success.html', {'success': email_is_sent})

    def hrefs_from_cart(self):
        # extracts list of products from cart, and return them as list of http links (in json format)
        if not 'cart' in self.request.session:
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


def cart_count_request(request):
    # returns count of items in request cart (ajax only).
    if not 'cart' in request.session:
        return HttpResponse("0")
    else:
        return HttpResponse(len(request.session['cart']))


def media_backup_filter(filename):
    # filter for media dir archiving function
    if '__sized__' in filename.path:
        return None
    return filename


@staff_member_required
def media_backup_request(request):
    # returns gzipped content of /media directory
    resp = HttpResponse(content_type='application/x-gzip')
    resp['Content-Disposition'] = 'attachment; filename=media_{}.tar.gz'.format(
        (datetime.now().isoformat()).split('.')[0], )
    with tarfile.open(fileobj=resp, mode='w:gz') as tar:
        tar.add(settings.MEDIA_ROOT, filter=media_backup_filter)
    return resp


class LangRedirect(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        # for english language - redirect to /partners page, for others - return current page
        if self.request.LANGUAGE_CODE == 'en':
            return reverse('partners')
        else:
            curr_path = self.request.GET.get('curr_path')
            if curr_path:
                if curr_path == '/en/partners/':
                    curr_path = '/ru/partners/'
                return curr_path
            else:
                return reverse('main')


class SubscribeView(FormView):
    template_name = 'subscribe_msg.html'
    form_class = SubscriberForm

    def form_valid(self, form):
        if form.is_valid():
            Subscriber.objects.create(email=form.cleaned_data['email'])
            return render(self.request, 'subscribe_msg.html', {'success': True})


@staff_member_required
def get_subscribers(request):
    # returns list of subscribers in csv format
    resp = HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="subscribers_{}.csv"'.format(
        (datetime.now().isoformat()).split('.')[0], )
    writer = csv.writer(resp)
    writer.writerow(['email'])
    for item in Subscriber.objects.filter(is_active=True):
        writer.writerow([item.email])
    return resp
