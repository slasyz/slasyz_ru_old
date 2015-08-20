{% load i18n %}
{% load include_if_exists %}

<nav id="topbar" class="top-bar" data-topbar role="navigation">
    <ul class="title-area">
        <li class="name">
            <h1></h1>
        </li>
        <li class="toggle-topbar menu-icon"><a href="#"><span></span></a></li>
    </ul>

    <section class="top-bar-section">
        <ul class="left">
            {% for key, value in APPS %}
                {% comment %} TODO: add app permission check{% endcomment %}
                <li>{% include 'global/tpl/topbar_link.tpl' with url_name=key|add:":index" caption=value.short_title %}</li>
            {% endfor %}
        </ul>

        <ul class="right">
            {% if user.is_authenticated %}
                <li><a class="disabled">{% trans "Hello" %}, {{ user.first_name }} {{ user.last_name }}!</a></li>
            {% endif %}

            {% include_if_exists APP_NAME|add:"/global/topbar_app_links.tpl" %}

            {% if user.is_authenticated %}
                <li><a href="{% url 'logout' %}">{% trans 'Logout' %}</a></li>
            {% else %}
                <li>{% include 'global/tpl/topbar_link.tpl' with url_name='login' caption='Login' url_params='next='|add:request.path %}</li>
            {% endif %}
        </ul>
    </section>
</nav>