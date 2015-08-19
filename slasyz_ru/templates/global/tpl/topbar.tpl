{% load i18n %}
{% load include_if_exists %}

<div id="topbar" class="bar">
    <div class="row">
        <div class="small-12 columns">
            <ul class="bar-left">
                {% for key, value in APPS %}
                    {% comment %}TODO: add app permission check{% endcomment %}
                    <li>{% include 'global/tpl/topbar_link.tpl' with url_name=key|add:":index" caption=value.short_title %}</a></li>
                {% endfor %}
            </ul>
            <ul class="bar-right">
                {% if user.is_authenticated %}
                    <li><span class="bar-element">{% trans "Hello" %}, {{ user.first_name }} {{ user.last_name }}!</span></li>
                {% endif %}

                {% include_if_exists APP_NAME|add:"/global/topbar_app_links.tpl" %}

                {% if user.is_authenticated %}
                    <li><a class="bar-element" href="{% url 'logout' %}">{% trans 'Logout' %}</a></li>
                {% else %}
                    <li>{% include 'global/tpl/topbar_link.tpl' with url_name='login' caption='Login' url_params='next='|add:request.path %}</li>
                {% endif %}
            </ul>
        </div>
    </div>
</div>
