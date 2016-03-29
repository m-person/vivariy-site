# -*- coding: utf-8 -*-
from django import template
from app.models import Product
from urllib.parse import urlparse
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag
def default_image(product):
    """
    Returns default image for Product.
    Simply returns result of Product.images.filter(is_default=True) or first image if default doesn`t exist.
    """
    if not isinstance(product, Product):
        return ''
    try:
        return product.images.filter(is_default=True)[0]
    except IndexError:
        if product.images.all().count() > 0:
            return product.images.all()[0]
        else:
            return ''


@register.filter
@stringfilter
def domain_from_url(url):
    """
    Extracts domainname from url
    :return: (string): shortened url like http(s)://<domainname>.<tld>
    """
    if len(url) == 0:
        return ''
    try:
        u1 = urlparse(url)
        return '{}://{}'.format(u1.scheme, u1.netloc)
    except AttributeError:
        return ''

