# coding: utf-8

from django.conf.urls import patterns, include, url
from slasyz_ru.settings import static

# по идее, эта херня должна дублироваться в конфигах апача-нджинкса-чтонибудьещё

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'slasyz_ru.views.home', name='home'),
    # url(r'^slasyz_ru/', include('slasyz_ru.foo.urls')),

    url(r'^$', 'slasyz_ru.views.index'),
    url(r'^upload/', include('upload.urls')),

    url(r'^400$', 'slasyz_ru.views.custom_400'),
    url(r'^403$', 'slasyz_ru.views.custom_403'),
    url(r'^404$', 'slasyz_ru.views.custom_404'),
    url(r'^500$', 'slasyz_ru.views.custom_500'),

    # This should be in your proxy (i.e. nginx) config
    url(r'^static\/(?P<path>.*)$', 'django.views.static.serve', {'document_root': static(__file__)}),
)

handler400 = 'slasyz_ru.views.custom_400'
handler403 = 'slasyz_ru.views.custom_403'
handler404 = 'slasyz_ru.views.custom_404'
handler500 = 'slasyz_ru.views.custom_500'
