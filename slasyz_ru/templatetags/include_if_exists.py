from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def include_if_exists(context, template_name):
    try:
        # Loading the template and rendering it
        included_template = template.loader.get_template(template_name).render(context)
    except template.TemplateDoesNotExist:
        included_template = ''
    return included_template
