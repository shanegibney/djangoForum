from django.contrib.auth.models import User
from django import template
register = template.Library()

@register.inclusion_tag("results.html")
def results(poll):
    active_users = User.objects.all().filter(is_active = True)
    return {'active_users': active_users}
