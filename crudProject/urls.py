from django.conf.urls import url, include
from django.contrib import admin
from crudapp import views as home

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^$', home.init, name='init'),
    url(r'^edit/(?P<id>\d+)/$', home.edit, name='edit'),
    url(r'^delete/(?P<id>\d+)/$', home.delete, name='delete'),
    # url(r'^thread/(?P<id>\d+)/(?P<topic>\d+)/$', home.thread, name='thread'),
    url(r'^thread/(?P<id>\d+)/$', home.thread, name='thread'),
    url(r'^topic_form/$', home.topic_form, name='topic_form'),
    url(r'^todo/$', home.todo, name='todo'),
    url(r'^profile/(?P<id>\d+)/$', home.profile, name='profile'),
    url(r'^contact/$', home.contact, name='contact'),
    url(r'^tinymce/', include('tinymce.urls')),
    # url(r'^delete/(?P<id>\d+)/$', home.delete_new, name='delete_new'),

    # example from wearesocial
    # url(r'^post/delete/(?P<thread_id>\d+)/(?P<post_id>\d+)/$', forum_views.delete_post, name='delete_post'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    ]
