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
                    <li>{% include 'global/tpl/bar_link.tpl' with url_name='management_blog_add' caption='New post' %}</li>
                    <li><a class="bar-element" href="{% url 'logout' %}">{% trans 'Logout' %}</a></li>
                {% else %}
                    <li>{% include 'global/tpl/bar_link.tpl' with url_name='login' caption='Login' %}</li>
                {% endif %}
            </ul>
        </div>
    </div>
</div>
