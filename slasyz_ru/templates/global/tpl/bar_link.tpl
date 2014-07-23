{% load i18n %}

{% url url_name as the_url %}

<a class="bar-element{% if request.path == the_url %} current{% endif %}" href="{% url url_name %}">{% trans caption %}</a>
