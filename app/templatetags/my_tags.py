# -*- coding: utf-8 -*-
from django import template
from app.models import Product

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
