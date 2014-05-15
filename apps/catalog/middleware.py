# -*- coding: utf-8 -*-

from .models import SiteTowns


class SiteTownsMiddleware(object):
#     '''Add order attribute to request only if appropriate Order instance exists'''
#
    def process_request(self, request):
        city = request.session.get('city')
        if not city:
            main_city = SiteTowns.objects.filter(is_active=True)[:1].get()
            request.session['city'] = main_city
