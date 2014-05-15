from django.conf.urls import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from common.views import Main_Page

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^imperavi/', include('imperavi.urls')),
                       (r'^grappelli/', include('grappelli.urls')),
                       url(r'^cked/', include('cked.urls')),
                       url(r'^cart/', include('cart.urls', namespace='cart')),
                       url(r'^catalog/', include('catalog.urls', namespace='catalog')),
                       url(r'^compare/', include('compare.urls', namespace='compare')),
                       url(r'^feedback/', include('feedback.urls', namespace='feedback')),
                       url(r'^flatpages/', include('flatpages.urls', namespace='flatpages')),
                       url(r'^pricelist/', include('pricelist.urls', namespace='pricelist')),
                       url(r'^search/', include('common.urls', namespace='common')),

                       url(r'^contact/$', 'flatpages.views.flatpage', {'url': '/contact/'}, name='contact'),
                       url(r'^about/$', 'flatpages.views.flatpage', {'url': '/about/'}, name='about'),
                       url(r'^delivery/$', 'flatpages.views.flatpage', {'url': '/delivery/'}, name='delivery'),
                       url(r'^payment/$', 'flatpages.views.flatpage', {'url': '/payment/'}, name='payment'),
                       url(r'^questions/$', 'flatpages.views.flatpage', {'url': '/questions/'}, name='questions'),
                       url(r'^wholesale_department/$', 'flatpages.views.flatpage', {'url': '/wholesale_department/'},
                           name='wholesale_department'),
                       url(r'^page(?P<url>.*)$', 'flatpages.views.flatpage', name='page'),


                       url(r'^$', Main_Page.as_view(), name='index'),

                       url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT}),
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.STATICFILES_DIRS}),
    )

handler403 = 'common.views.Error403'
handler404 = 'common.views.Error404'
handler500 = 'common.views.Error500'

