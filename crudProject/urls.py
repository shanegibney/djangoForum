from django.conf.urls import url, include
from django.contrib import admin
from crudapp import views as home
from fileuploader import views as fileshare
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns


urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^$', home.init, name='init'),
    url(r'^edit/(?P<id>\d+)/$', home.edit, name='edit'),
    url(r'^delete/(?P<id>\d+)/$', home.delete, name='delete'),
    # passing two id's in a url
    # url(r'^thread/(?P<id>\d+)/(?P<topic>\d+)/$', home.thread, name='thread'),
    url(r'^thread/(?P<id>\d+)/$', home.thread, name='thread'),
    url(r'^topic_form/$', home.topic_form, name='topic_form'),
    url(r'^todo/$', home.todo, name='todo'),
    url(r'^blog/$', home.blog, name='blog'),
    url(r'^file_sharing/$', fileshare.file_sharing, name='file_sharing'),
    url(r'^file_sharing_form/$', fileshare.file_sharing_form, name='file_sharing_form'),
    url(r'^blog_form/$', home.blog_form, name='blog_form'),
    url(r'^site_users/$', home.site_users, name='site_users'),
    url(r'^profile/(?P<id>\d+)/$', home.profile, name='profile'),
    url(r'^media/(?P<path>\d+)/$', 'django.views.static.serve', name='media'),
    url(r'^profile_contact/(?P<id>\d+)/$', home.profile_contact, name='profile_contact'),
    url(r'^contact/$', home.contact, name='contact'),
    url(r'^tinymce/', include('tinymce.urls')),

    # url(r'^post/delete/(?P<thread_id>\d+)/(?P<post_id>\d+)/$', forum_views.delete_post, name='delete_post'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    ]

if settings.DEBUG:
    urlpatterns += patterns('', url(r'^media/(?P<path>)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),)

# if settings.DEBUG is True:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
