{% load i18n %}

<div id="topbar" class="bar">
    <div class="row">
        <div class="small-12 columns">
            <ul class="bar-left">
                {% if user.is_authenticated %}
                    <li>{% include 'global/tpl/bar_link.tpl' with url_name='management' caption='Management' %}</a></li>
                {% endif %}
                <li>{% include 'global/tpl/bar_link.tpl' with url_name='upload' caption='Upload' %}</a></li>
                <li>{% include 'global/tpl/bar_link.tpl' with url_name='blog' caption='Blog' %}</li>
            </ul>
            <ul class="bar-right">
                {% if user.is_authenticated %}
                    <li><span class="bar-element">{% trans "Hello" %}, {{ user.first_name }} {{ user.last_name }}!</span></li>
                {% endif %}

                <!-- {{ TOPBAR_LINKS }} -->
                {% for link in TOPBAR_LINKS %}
                    {% comment %}because django template system cannot into parentheses inside "if" tag{% endcomment %}
                    {% if not link.needs_auth %}
                        <li>{% include 'global/tpl/bar_link.tpl' with url_name=link.url caption=link.caption %}</li>
                    {% endif %}
                    {% if user.is_authenticated and not user.is_superuser and link.needs_auth and not link.needs_admin %}
                        <li>{% include 'global/tpl/bar_link.tpl' with url_name=link.url caption=link.caption %}</li>
                    {% endif %}
                    {% if user.is_authenticated and user.is_superuser and link.needs_auth and link.needs_admin %}
                        <li>{% include 'global/tpl/bar_link.tpl' with url_name=link.url caption=link.caption %}</li>
                    {% endif %}
                {% endfor %}

                {% if user.is_authenticated %}
                    <li><a class="bar-element" href="{% url 'logout' %}">{% trans 'Logout' %}</a></li>
                {% else %}
                    <li>{% include 'global/tpl/bar_link.tpl' with url_name='login' caption='Login' %}</li>
                {% endif %}
            </ul>
        </div>
    </div>
</div>
