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
    </div>
    <div class="text">{{ comment.text }}</div>
</div>
