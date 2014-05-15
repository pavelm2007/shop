from django import template
from django.db.models.loading import get_model
from django.conf import settings

from catalog.models import Category, Product, SiteTowns

register = template.Library()


@register.assignment_tag()
def get_root_category():
    # qs = Category.tree.root_nodes()
    qs = Category.objects.filter(main_page=True, parent=None, is_active=True)
    return qs

@register.assignment_tag()
def root_category():
    # qs = Category.tree.root_nodes()
    qs = Category.objects.filter(parent=None, is_active=True)
    return qs


@register.assignment_tag
def product_mark(pk):
    obj = Product.objects.get(pk=pk)
    if obj.is_deal:
        return u'icon-prosent.png'
    if obj.is_popular:
        return u'icon-best.png'
    if obj.is_novelty:
        return u'icon-new.png'


@register.assignment_tag()
def site_city():
    qs = SiteTowns.objects.filter(is_active=True)
    return qs

@register.assignment_tag()
def site_city_main():
    qs = SiteTowns.objects.filter(is_active=True)[:1].get()
    return qs
