{% if perms.post.add %}
    <li>{% include 'global/tpl/bar_link.tpl' with url_name="upload_filesystem" caption="Filesystem" %}</li>
{% endif %}
