from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
# from django.db import models
# from .models import FileModel
from fileuploader.models import FileModel
# from wherever import get_all_logged_in_users
from django import template
register = template.Library()
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@register.inclusion_tag('sidebar_files.html', takes_context=True)
def file_sharing_sidebar(context):
    request = context['request']
    filemodel = FileModel.objects.all().reverse()
    paginator = Paginator(filemodel, 3)
    page = request.GET.get('file')
    try:
        file_model = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        file_model = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        file_model = paginator.page(paginator.num_pages)
    context = {'file_model': file_model}
    return {'file_model': file_model, 'current_time': timezone.now()}
    # return render(request, 'sidebar_files.html', context)

# @register.inclusion_tag("results.html")
# def results(poll):
#     active_users = User.objects.all().filter(is_active = True)
#     return {'active_users': active_users}


# def get_all_logged_in_users():
#     # Query all non-expired sessions
#     # use timezone.now() instead of datetime.now() in latest versions of Django
#     sessions = Session.objects.filter(expire_date__gte=timezone.now())
#     uid_list = []
#
#     # Build a list of user ids from that query
#     for session in sessions:
#         data = session.get_decoded()
#         uid_list.append(data.get('_auth_user_id', None))
#
#     # Query all logged in users based on id list
#     return User.objects.filter(id__in=uid_list)


# @register.inclusion_tag('results.html')
# def render_logged_in_user_list():
#     return { 'users': get_all_logged_in_users() }
