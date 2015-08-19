{% if perms.post.add %}
    <li>{% include 'global/tpl/topbar_link.tpl' with url_name="admin:blog_post_add" caption="New post" %}</li>
{% endif %}
