from django.conf import settings
from django.views.generic import TemplateView, DetailView, ListView, View
from django.forms.models import model_to_dict
from braces.views import JSONResponseMixin

from catalog.models import Product, Category, SiteTowns


__all__ = [
    'Index',
    'ProductDetail',
    'ProductList',
    'robots',

    'CatalogCity',
]


class CatalogMixin(object):
    model_name = None
    current_category = None
    categories = None
    city = None

    def __init__(self):
        self.categories = Category.active.all()
        super(CatalogMixin, self).__init__()

    def dispatch(self, request, *args, **kwargs):
        city = SiteTowns.objects.get(name=request.session['city'])
        self.city = city
        return super(CatalogMixin, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        ctx = super(CatalogMixin, self).get_context_data(**kwargs)
        # categories = Category.active.all()
        ctx.update(
            {
                'category_list': self.categories,
            }
        )
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            current_category = self.categories.get(slug=category_slug)
            root_cat = current_category.get_root()
            ctx.update(
                {
                    'current_category': current_category,
                    'root_cat':root_cat,
                }
            )
        return ctx


class Index(CatalogMixin, TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        ctx = super(Index, self).get_context_data(**kwargs)
        # ctx = CatalogMixin.get_context_data(self,**kwargs)
        deals = Product.active.get_city_object(self.city).filter(is_deal=True)[:15]
        popular = Product.active.get_city_object(self.city).filter(is_popular=True)[:15]
        novelty = Product.active.get_city_object(self.city).filter(is_novelty=True)[:15]
        ctx.update(
            {
                'deals': deals,
                'popular': popular,
                'novelty': novelty,
            }
        )
        return ctx


class ProductList(CatalogMixin, ListView):
    model = Product
    template_name = 'catalog/list.html'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')

        if category_slug:
            current_category = self.categories.get(slug=category_slug)
            descendants = current_category.get_descendants(include_self=True)
            qs = self.model.active.get_city_object(self.city).filter(category__in=descendants)
        else:
            qs = self.model.active.get_city_object(self.city).all()
        return qs


class ProductDetail(CatalogMixin, DetailView):
    model = Product
    template_name = 'catalog/detail.html'

    def get_context_data(self, **kwargs):
        ctx = super(ProductDetail, self).get_context_data(**kwargs)
        current_category = self.get_object().category
        root_cat = current_category.get_root()
        ctx.update(
            {
                'current_category': self.get_object().category,
                'root_cat':root_cat,
            }
        )
        return ctx


class CatalogCity(JSONResponseMixin, View):
    model = SiteTowns

    def get(self, request, *args, **kwargs):
        city_pk = self.kwargs.get('pk')
        city = self.model.objects.get(pk=city_pk)
        if city:
            request.session['city'] = city
            request.session.modified = True
        context_dict = model_to_dict(city)

        return self.render_json_response(context_dict)


def robots(request):
    from django.http import HttpResponse

    if settings.SITE_PUBLIC:
        return HttpResponse("User-agent: *\nDisallow: /admin/\nSitemap: http://%s/sitemap.xml" % request.get_host(),
                            mimetype="text/plain")
    else:
        return HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")