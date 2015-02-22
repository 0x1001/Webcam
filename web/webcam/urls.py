from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webcam.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'home.views.home'),
    url(r'^recordings$', 'home.views.recordings'),
    url(r'^watch/(?P<file_name>[\w\.]+)$', 'home.views.recordings'),
    url(r'^admin/', include(admin.site.urls)),
)
