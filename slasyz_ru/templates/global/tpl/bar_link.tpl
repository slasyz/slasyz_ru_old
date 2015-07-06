{% load i18n %}
{% load startswith %}

{% url url_name as the_url %}
<!-- url = {{ url_name }} -->
<a class="bar-element{% if request.path|startswith:the_url %} active{% endif %}" href="{{ the_url }}{% if url_params %}?{{ url_params }}{% endif %}">{% trans caption %}</a>
