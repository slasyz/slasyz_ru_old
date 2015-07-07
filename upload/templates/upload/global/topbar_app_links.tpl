{% if perms.post.add %}
    <li>{% include 'global/tpl/bar_link.tpl' with url_name="upload:filesystem" caption="Filesystem" %}</li>
{% endif %}
