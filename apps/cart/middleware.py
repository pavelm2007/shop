# -*- coding: utf-8 -*-

import re

from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from .settings import CART_OPTIONS_USE_DELETE
from .models import Order


_CART_JS_RE = \
    re.compile(r'(<script\W[^>]*\bsrc\s*=\s*(\'|"|)[^\'^\"]*jquery.cart.js(\'|"|)\b[^>]*>\W*</\s*script\s*>)',
               re.IGNORECASE)
CART_URL_SCRIPT = '''
<script type="text/javascript">
cart.add_url = '%(add)s';
cart.del_url = '%(del)s';
</script>
'''


class CartMiddleware(object):
    '''Add order attribute to request only if appropriate Order instance exists'''

    def process_request(self, request):
        if request.user.is_authenticated():
            if request.user.order_set.filter(status=1).count() == 1:
                request.order = request.user.order_set.filter(status=1).get()
                request.session['order_id'] = request.order.id
            elif request.user.order_set.filter(status=1).count() == 0:
                request.order = None
            else:
                # exception situation, two orders created!
                request.order = request.user.order_set.filter(status=1)[0]
                request.session['order_id'] = request.order.id
        else:
            if 'order_id' in request.session:
                try:
                    request.order = Order.objects.filter(status=1).get(
                        id=request.session['order_id'])
                except ObjectDoesNotExist:
                    # Order completed
                    del request.session['order_id']
                    request.order = None
            else:
                request.order = None


    def process_response(self, request, response):
        '''Add basket url to script'''
        urls = {
            'add': reverse('cart:show_cart'),
        }
        if CART_OPTIONS_USE_DELETE:
            urls['del'] = reverse('cart:show_cart')
        else:
            urls['del'] = ''
        try:
            def add_url_definition(match):
                return mark_safe(match.group() + CART_URL_SCRIPT % urls)

            response.content = _CART_JS_RE.sub(add_url_definition, response.content)
        except:
            return response
        else:
            return response
