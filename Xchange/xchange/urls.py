from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'xchange.views.home'),
    url(r'^home$', 'xchange.views.home', name = 'home'),
    url(r'^profile/(?P<id>\d+)$', 'xchange.views.profile', name = 'profile'),
    url(r'^edit_profile$', 'xchange.views.edit_profile', name = 'edit_profile'),
    url(r'^add-item$', 'xchange.views.add_item', name = 'add_item'),
    #url(r'^delete-item/(?P<id>\d+)$', 'xchange.views.delete_item'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'xchange/login.html'}, name = 'login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name = 'logout'),
    url(r'^register$', 'xchange.views.register', name = 'register'),
    url(r'^photo/(?P<id>\d+)$', 'xchange.views.photo', name = 'photo'),
    url(r'^follow/(?P<id>\d+)$', 'xchange.views.follow', name = 'follow'),
    url(r'^unfollow/(?P<id>\d+)$', 'xchange.views.unfollow', name = 'unfollow'),
    url(r'^followstream$', 'xchange.views.followstream', name = 'followstream'),
    url(r'^get_post_json$', 'xchange.views.get_post_json'),
    url(r'^comment/(?P<id>\d+)$', 'xchange.views.comment', name = 'comment'),
    url(r'^comment_form/(?P<id>\d+)$', 'xchange.views.comment_form', name = 'comment_form'),
)
