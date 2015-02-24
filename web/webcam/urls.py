from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'home.views.home'),
    url(r'^recordings$', 'home.views.recordings'),
    url(r'^watch/(?P<file_name>[\w\.]+)$', 'home.views.watch'),
    url(r'^configuration$', 'home.views.get_config'),
    url(r'^stream$', 'home.views.stream'),
    url(r'^admin/', include(admin.site.urls)),
)
