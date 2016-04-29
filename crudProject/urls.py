from django.conf.urls import url
from django.contrib import admin
from crudapp import views as home

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^$', home.init, name='init'),
    url(r'^edit/(?P<id>\d+)/$', home.edit_new, name='edit_new'),
    url(r'^delete/(?P<id>\d+)/$', home.delete_new, name='delete_new'),
    url(r'^post/new/$', home.member_new, name='member_new'),

    # Auth-related URLs:
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^accounts/loggedin/$', 'crudProject.views.loggedin', name='loggedin'),

    # Registration URLs
    url(r'^accounts/register/$', 'crudProject.views.register', name='register'),
    url(r'^accounts/register/complete/$', 'crudProject.views.registration_complete', name='registration_complete'),
    ]
