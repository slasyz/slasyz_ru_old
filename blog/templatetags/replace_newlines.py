from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='replace_newlines')
@stringfilter
def replace_newlines(value):
    return '<p>' + value.replace('\r\n', '\n').replace('\r', '\n').replace('\n\n', '</p><p>') + '</p>'
