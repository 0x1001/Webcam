from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'home.views.home'),
    url(r'^recordings$', 'home.views.recordings'),
    url(r'^recordings/(?P<recording>[\w\.]+)$', 'home.views.recordings'),
    url(r'^photos$', 'home.views.photos'),
    url(r'^photos/(?P<photo>[\w\.]+)$', 'home.views.photos'),
    url(r'^photos/(?P<page>[\d]+)/(?P<photo>[\w\.]+)$', 'home.views.photos'),
    url(r'^movements$', 'home.views.movements'),
    url(r'^movements/(?P<page>[\d]+)$', 'home.views.movements'),
    url(r'^configuration$', 'home.views.get_config'),
    url(r'^stream$', 'home.views.stream'),
    url(r'^stream_data$', 'home.views.stream_data'),
    url(r'^admin/', include(admin.site.urls)),
)
