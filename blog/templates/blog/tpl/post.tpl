{% load i18n %}

<div class="post">
    <h3 class="title"><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></h3>
    <div class="text">
        {{ post.annotation.rendered|safe }}
        {% if full %}
            <div id="cut"></div>
            {{ post.full_text.rendered|safe }}
        {% endif %}
    </div>
    <div class="info">
        {% trans "created in" %} {{ post.created }}
        | <a href="{{ post.get_absolute_url }}#comments">
              {% blocktrans with count=post.get_comments_count %}{{ count }} comments{% endblocktrans %}
          </a>
        {% if user.is_superuser %}
            | <a href="{% url 'admin:blog_post_change' post.id %}">edit</a>
            | <a href="{% url 'admin:blog_post_delete' post.id %}">rm</a>
        {% endif %}
    </div>
</div>
