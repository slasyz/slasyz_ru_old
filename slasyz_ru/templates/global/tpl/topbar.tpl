{% load i18n %}

<div id="topbar" class="bar">
    <div class="row">
        <div class="small-12 columns">
            <ul class="bar-left">
                {% for key, value in APPS %}
                    {% if not value.needs_admin or user.is_superuser %}
                        <li>{% include 'global/tpl/bar_link.tpl' with url_name=key caption=value.short_title %}</a></li>
                    {% endif %}
                {% endfor %}
            </ul>
            <ul class="bar-right">
                {% if user.is_authenticated %}
                    <li><span class="bar-element">{% trans "Hello" %}, {{ user.first_name }} {{ user.last_name }}!</span></li>
                {% endif %}

                {% for link in APP_INFO.topbar_links %}
                    {% if not link.needs_auth or user.is_superuser or not link.needs_admin and user.is_authenticated %}
                        <li>{% include 'global/tpl/bar_link.tpl' with url_name=link.url caption=link.caption %}</li>
                    {% endif %}
                {% endfor %}

                {% if APP_NAME %}
                    {% comment %}TODO: remove it with management app{% endcomment %}
                    {% url 'management_'|add:APP_NAME as app_manage_url %}
                    {% if user.is_superuser and app_manage_url %}
                        <li><a class="bar-element" href="{{ app_manage_url }}">Manage</a></li>
                    {% endif %}
                {% endif %}

                {% if user.is_authenticated %}
                    <li><a class="bar-element" href="{% url 'logout' %}">{% trans 'Logout' %}</a></li>
                {% else %}
                    <li>{% include 'global/tpl/bar_link.tpl' with url_name='login' caption='Login' %}</li>
                {% endif %}
            </ul>
        </div>
    </div>
</div>
