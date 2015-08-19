{% load i18n %}
{% load startswith %}

{% url url_name as the_url %}
<li{% if request.path|startswith:the_url %} class="active"{% endif %}><a href="{{ the_url }}{% if url_params %}?{{ url_params }}{% endif %}">{% trans caption %}</a></li>
