<div class="post">
    <h3 class="title">{{ post.title }}</h3>
    <span class="info">created in {{ post.created }}</span>
    <div class="text">{{ post.text|safe }}</div>
</div>