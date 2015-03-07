from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^', include('xchange.urls')),
    #url(r'^$', 'xchange.views.home'),
)
