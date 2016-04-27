"""crudProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from crudapp import views as home

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^$', home.init, name='init'),
    # url(r'^details/', home.details),
    # url(r'^contact/', home.get_name),
    url(r'^edit/(?P<id>\d+)/$', home.edit_new, name='edit_new'),
    url(r'^delete/(?P<id>\d+)/$', home.delete_new, name='delete_new'),
    url(r'^post/(?P<pk>\d+)/$', home.post_detail, name='post_detail'),
    url(r'^post/new/$', home.member_new, name='member_new'),
    # url(r'^display_meta/', home.display_meta),
]
