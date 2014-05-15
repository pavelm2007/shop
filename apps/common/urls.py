from django.conf.urls import *

from .views import search_product, Search_result, SearchList

urlpatterns = patterns('',
                       url(r'^$', search_product, name='search_product'),
                       url(r'^sended/$', Search_result.as_view(),
                           name='search_result'),
                       url(r'^api/search/$', SearchList.as_view(),
                           name='search_list'),

)


