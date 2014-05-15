from django.conf.urls import patterns, url
from django.contrib import sitemaps
from catalog.sitemap import ProductSitemap, CategorySitemap

from .views import *

urlpatterns = patterns('',
                       url(r'^$', Index.as_view(), name='index'),
                       url(r'^(?P<category_slug>[\w-]+)$', ProductList.as_view(), name='category'),
                       url(r'^(?P<slug>[\w-]+).html$', ProductDetail.as_view(), name='product')
)

urlpatterns += patterns('',
                        url(r'^api/(?P<pk>\d).html$', CatalogCity.as_view(), name='catalog_city')
)

sitemaps = {
    "categories": CategorySitemap,
    "products": ProductSitemap
}

urlpatterns += patterns('',
                        url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
                        url(r'^robots\.txt$', 'catalog.views.robots'),
)
