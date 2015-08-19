{% load i18n %}

<div class="post">
    <h3 class="title">
        {% if post.is_draft %}
            <span class="draft">[{% trans "draft" %}]</span>
        {% endif %}
        <a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
    </h3>
    <div class="text">
        {{ post.annotation.rendered|safe }}
        {% if full %}<br><br>
            <div id="cut"></div>
            {{ post.full_text.rendered|safe }}
        {% endif %}
    </div>
    <div class="info">
        {{ post.created }}
        {% if post.tags.count %}
            | Tags: {% for tag in post.tags.all %}
                        <a href="{% url 'blog:tag' tag.name %}">{{ tag.name }}</a>
                    {% endfor %}
        {% endif %}
        | <a href="{{ post.get_absolute_url }}#comments">
              {% blocktrans with count=post.get_comments_count %}{{ count }} comments{% endblocktrans %}
          </a>

        {% if perms.blog.change %}
            | <a href="{% url 'admin:blog_post_change' post.id %}">edit</a>
        {% endif %}
        {% if perms.blog.delete %}
            | <a href="{% url 'admin:blog_post_delete' post.id %}">del</a>
        {% endif %}
    </div>
</div>
