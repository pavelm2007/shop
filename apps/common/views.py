# -*- coding: utf-8 -*-
import re
from django.views.generic import TemplateView, View
from django.db.models import Q

from braces.views import JSONResponseMixin, AjaxResponseMixin

from catalog.models import Product, Producer

from .utils import render_to


class Main_Page(TemplateView):
    template_name = 'index.html'


class SearchList(JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        q = request.GET.get('query', '').strip()

        q = re.sub(r'\s+', ' ', q)

        words = []
        for w in q.split(' '):
            if len(w) > 1:
                words.append(w)

        filters = Q()

        for w in words:
            filters &= Q(name__icontains=w)
            # product_qs = dict(Product.active.filter(filters).order_by('name').distinct().values_list('pk', 'name')[:20])
        product_qs = Product.active.filter(filters).order_by('name').distinct()[:20]
        suggestion=[]
        data = []
        for p in product_qs:
            suggestion.append(p.name)
            data.append(p.pk)
        json_dict = {'query': q,
                     'suggestions': suggestion,
                     'data': data}
        return self.render_json_response(json_dict)


@render_to('common/search_result.html')
def search_product(request):
    q = request.GET.get('query_field', '').strip()
    q = re.sub(r'\s+', ' ', q)
    # if request.is_ajax():
    #     if len(q) < 2:
    #         return JsonResponse([])
    # elif len(q) < 2:
    #     return render_to_response('catalog/search.html', {'empty_request': True}, context_instance=RequestContext(request))

    words = []
    for w in q.split(' '):
        if len(w) > 1:
            words.append(w)

    # producers
    filters = Q()
    for w in words:
        filters &= Q(name__icontains=w)
    producers = Producer.objects.filter(filters).order_by('name')
    for w in words:
        filters &= Q(name__icontains=w) | Q(SKU__icontains=w) | Q(producer__name__icontains=w)
    product_qs = Product.active.filter(filters).order_by('name').distinct()

    # results = []
    # if producers:
    #     results.append((u'Производители', producers))
    # if product:
    #     results.append((u'Товары', product))

    res = {
        'site_search_q': q,
        'results': product_qs,
        'count_result': product_qs.count()
    }
    return res


class Search_result(TemplateView):
    pass


def robots(request):
    from django.http import HttpResponse

    return HttpResponse("User-agent: *\nDisallow: /admin/\nSitemap: http://%s/sitemap.xml" % request.get_host(),
                        mimetype="text/plain")


class Error403(TemplateView):
    template_name = '404.html'


class Error404(TemplateView):
    template_name = '404.html'


class Error500(TemplateView):
    template_name = '500.html'