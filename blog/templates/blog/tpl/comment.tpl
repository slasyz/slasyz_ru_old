{% load i18n %}

<div class="comment" id="comment-{{ comment.id }}">
    <div class="info">
        <a href="{{ comment.get_absolute_url }}">#</a>
        {% if comment.author %}
            <span class="name">{{ comment.author.first_name }} {{ comment.author.last_name }}</span>,
        {% else %}
            <span class="name">{{ comment.author_name }}</span>,
        {% endif %}
        <span class="date">{{ comment.created }}</span>
        {% if user.is_superuser %}
            | <a href="{% url 'admin:blog_comment_change' comment.id %}">edit</a>
            | <a href="{% url 'admin:blog_comment_delete' comment.id %}">rm</a>
        {% endif %}
    </div>
    <div class="text">{{ comment.text.rendered|safe }}</div>
</div>
