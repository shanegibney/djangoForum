from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
# from wherever import get_all_logged_in_users
from django import template
register = template.Library()

# @register.inclusion_tag("results.html")
# def results(poll):
#     active_users = User.objects.all().filter(is_active = True)
#     return {'active_users': active_users}


def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(id__in=uid_list)


@register.inclusion_tag('results.html')
def render_logged_in_user_list():
    return { 'users': get_all_logged_in_users() }
