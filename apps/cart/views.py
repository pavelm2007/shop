# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_http_methods
from django.template import RequestContext
from django.template.loader import render_to_string

import cart
# from checkout import checkout
from common.utils import render_to, JsonResponse

from .forms import OrderFormset, DefaultOrderForm

BASKET_OPTIONS_USE_KEEP = True


@csrf_exempt
@require_http_methods(["POST", "GET"])
@csrf_protect
@render_to('cart/cart.html', allow_ajax=True)
def cart_view(request, template_name="cart/cart.html"):
    """Представление для отображения корзины"""

    postdata = request.POST.copy()

    if request.method == 'POST':

        if postdata.has_key('add'):
            cart.add_to_cart(request)
            order = cart.get_cart(request)
            # res = {'order': order, }
            # html = render_to_string('cart/summary.html', res, context_instance=RequestContext(request))
            # return JsonResponse({
            #     'success': True,
            #     'action_add': True,
            #     'panel_html': html,
            # })
        if postdata.has_key('remove'):
            cart.remove_from_cart(request)

        if postdata.has_key('update'):
            cart.update_cart(request)

        if postdata.has_key('update') or postdata.has_key('remove') or postdata.has_key('add'):
            order = cart.get_cart(request)
            formset = OrderFormset(instance=order)
            res = {
                'order_form': DefaultOrderForm(request.POST),
                'formset': formset,
                'order': order,
                'keep': BASKET_OPTIONS_USE_KEEP,
                'delete': True,
            }
            html = render_to_string('cart/cart_table.html', res, context_instance=RequestContext(request))
            panel_html = render_to_string('cart/summary.html', res, context_instance=RequestContext(request))
            return JsonResponse({
                'success': True,
                # 'action_remove': True,
                'html': html,
                'panel_html': panel_html,
            })

        # if postdata.has_key('checkout'):
        #     checkout_url = checkout.get_checkout_url(request)
        #     return HttpResponseRedirect(checkout_url)
    # Получаем список всех товаров в корзине из cookies
    #cart_item_count = cart.cart_item_count(request)
    # cart_items = cart.get_cart_items(request)
    # cart_subtotal = cart.cart_subtotal(request)
    # return render_to_response(template_name, locals(),
    #                           context_instance=RequestContext(request))

    form = DefaultOrderForm(postdata or None)
    order = cart.get_cart(request)

    if form.is_valid() and order.goods > 0:
        contact = form.save(commit=False)
        contact.order = order
        contact.save()

        remote_address = request.META.get('REMOTE_ADDR')
        order.ip_address=remote_address
        order.status = 2
        order.save()

        return HttpResponseRedirect(reverse('cart:cart_confirm'))

    # else:
    #     return HttpResponseRedirect(reverse('cart:show_cart'))

    # order = cart.get_cart(request)
    formset = OrderFormset(instance=order)
    # form = DefaultOrderForm(postdata or None)
    return {
        'order_form': form,
        'formset': formset,
        'order': order,
        'keep': BASKET_OPTIONS_USE_KEEP,
        'delete': True,
    }


@csrf_exempt
@require_http_methods(["POST"])
@csrf_protect
@render_to('cart/checkout.html')
def checkout(request):
    postdata = request.POST.copy()
    form = DefaultOrderForm(postdata or None)
    order = cart.get_cart(request)

    if form.is_valid() and order.goods > 0:
        contact = form.save(commit=False)
        contact.order = order
        contact.save()
        order.status = 2
        order.save()
        return HttpResponseRedirect(reverse('cart:cart_confirm'))

    else:
        return HttpResponseRedirect(reverse('cart:show_cart'))

# @csrf_exempt
# @require_http_methods(["POST"])
# @csrf_protect
@render_to('cart/checkout.html')
def confirm(request):
    return {}