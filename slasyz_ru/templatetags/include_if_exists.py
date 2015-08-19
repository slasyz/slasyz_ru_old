from django.template import Library, TemplateDoesNotExist
from django.template.loader import get_template

register = Library()


@register.simple_tag(takes_context=True)
def include_if_exists(context, template_name):
    try:
        # Loading the template and rendering it
        included_template = get_template(template_name).render(context)
    except TemplateDoesNotExist:
        included_template = ''
    return included_template
