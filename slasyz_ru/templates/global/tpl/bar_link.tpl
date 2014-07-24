{% load i18n %}

{% url url_name as the_url %}
<a class="bar-element{% if request.path == the_url %} active{% endif %}" href="{{ the_url }}">{% trans caption %}</a>
