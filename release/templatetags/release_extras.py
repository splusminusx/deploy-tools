from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def index(l, i):
    return l[i]


@register.filter
@stringfilter
def status_color(status):
    if status == 'Successful':
        td = 'success'
    elif status == 'Failed':
        td = 'danger'
    elif status == 'Deploy in progress':
        td = 'active'
    elif status == 'New':
        td = 'info'
    elif status == 'Ready to deploy':
        td = 'warning '
    else:
        td = ''

    return td
