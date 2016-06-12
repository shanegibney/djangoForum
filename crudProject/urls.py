from django.conf.urls import url, include
from django.contrib import admin
from crudapp import views as home
from fileuploader import views as fileshare
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns
from django.contrib.staticfiles import views


urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^$', home.init, name='init'),
    url(r'^info/$', home.info, name='info'),
    url(r'^edit/(?P<id>\d+)/$', home.edit, name='edit'),
    url(r'^delete/(?P<id>\d+)/$', home.delete, name='delete'),
    url(r'^vote_up/(?P<id>\d+)/$', home.vote_up, name='vote_up'),
    url(r'^vote_down/(?P<id>\d+)/$', home.vote_down, name='vote_down'),
    url(r'^report/(?P<id>\d+)/$', home.report, name='report'),
    url(r'^vote_up_article/(?P<id>\d+)/$', home.vote_up_article, name='vote_up_article'),
    url(r'^vote_down_article/(?P<id>\d+)/$', home.vote_down_article, name='vote_down_article'),
    url(r'^vote_up_file/(?P<id>\d+)/$', fileshare.vote_up_file, name='vote_up_file'),
    url(r'^vote_down_file/(?P<id>\d+)/$', fileshare.vote_down_file, name='vote_down_file'),
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
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^profile_contact/(?P<id>\d+)/$', home.profile_contact, name='profile_contact'),
    url(r'^contact/$', home.contact, name='contact'),
    url(r'^tinymce/', include('tinymce.urls')),
    # url(r'^post/delete/(?P<thread_id>\d+)/(?P<post_id>\d+)/$', forum_views.delete_post, name='delete_post'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
