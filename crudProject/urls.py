from django.conf.urls import url
from django.contrib import admin
from crudapp import views as home
# from accounts import views as accounts_views

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^$', home.init, name='init'),
    url(r'^edit/(?P<id>\d+)/$', home.edit_new, name='edit_new'),
    url(r'^delete/(?P<id>\d+)/$', home.delete_new, name='delete_new'),
    url(r'^post/new/$', home.member_new, name='member_new'),
    ]
