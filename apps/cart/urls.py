# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url


urlpatterns = patterns('cart.views',
	# Просмотр корзины
	url(r'^$', 'cart_view', {'template_name':'cart/cart.html'}, name='show_cart'),
	url(r'^checkout/$', 'checkout', name='cart_checkout'),
	url(r'^confirm/$', 'confirm', name='cart_confirm'),

)
