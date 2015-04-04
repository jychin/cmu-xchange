from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webapps.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'xchange.views.stream',name="home"),
    url(r'^home$', 'xchange.views.stream', name = 'home'),
    url(r'^register/', 'xchange.views.register',name="register"),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'xchange/login.html'},name="login"),
    url(r'^stream/', 'xchange.views.stream',name="stream"),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login',name="logout"),
    url(r'^post/', 'xchange.views.post',name="post"),
    url(r'^profile/(?P<id>\d+)$', 'xchange.views.profile', name="profile"),
    url(r'^editprofile/', 'xchange.views.editprofile', name="editprofile"),
    url(r'^photo/(?P<id>\d+)$', 'xchange.views.get_photo', name="photo"),
    url(r'^itemphoto/(?P<id>\d+)$', 'xchange.views.get_itemphoto', name="itemphoto"),
    url(r'^follow/(?P<id>\d+)$', 'xchange.views.follow', name="follow"),
    url(r'^unfollow/(?P<id>\d+)$', 'xchange.views.unfollow', name="unfollow"),
    url(r'^followstream/', 'xchange.views.followstream',name="followstream"),
    url(r'^globalstreamjson/', 'xchange.views.globalstream_json',name="gsjson"),
    url(r'^addcomment/(?P<id>\d+)$', 'xchange.views.addcomment', name="addcomment"),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'xchange.views.confirm_registration', name='confirm'),
)
