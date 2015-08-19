{% load i18n %}

<div class="columns small-12">
    <a class="close-button" onclick="$(this).parent().remove();" title="Close">&times;</a>
    {% if error %}
        <span class="error-file">{{ short_name }}</span>
        <div class="error-text">{{ text }}</div>
    {% else %}
        <a class="success-file" href="{{ text }}">{{ short_name }}</a>
        <!--suppress HtmlFormInputWithoutLabel, HtmlFormInputWithoutLabel -->
        <input class="success-url" type="url" onclick="this.select();" value="{{ text }}" />
    {% endif %}
</div>
