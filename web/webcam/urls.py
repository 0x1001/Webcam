from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'home.views.home'),
    url(r'^' + settings.PREFIX + r'$', 'home.views.home'),
    url(r'^' + settings.PREFIX + r'about$', 'home.views.about'),
    url(r'^' + settings.PREFIX + r'movements$', 'home.views.movements'),
    url(r'^' + settings.PREFIX + r'movements/(?P<page>[\d]+)$', 'home.views.movements'),
    url(r'^' + settings.PREFIX + r'details/(?P<movement_id>[\d]+)$', 'home.views.movement_details'),
    url(r'^' + settings.PREFIX + r'stream$', 'home.views.stream'),
    url(r'^' + settings.PREFIX + r'stream_data$', 'home.views.stream_data'),
    url(r'^' + settings.PREFIX + r'configuration$', 'home.views.configuration'),
    url(r'^' + settings.PREFIX + r'configuration/restart_app$', 'home.views.restart_app'),
    url(r'^' + settings.PREFIX + r'configuration/restart_pi$', 'home.views.restart_pi'),
    url(r'^' + settings.PREFIX + r'configuration/shutdown_pi$', 'home.views.shutdown_pi'),
    url(r'^' + settings.PREFIX + r'admin/', include(admin.site.urls)),
)
