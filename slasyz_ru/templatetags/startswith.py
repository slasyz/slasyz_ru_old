from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='startswith')
@stringfilter
def startswith(value, arg):
    return value.startswith(arg)
