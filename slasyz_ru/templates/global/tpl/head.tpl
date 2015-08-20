<meta charset="utf-8" />
<link rel="shortcut icon" href="/favicon.png" type="image/png">
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{{ title }}{% if APP_INFO.title %} - {{ APP_INFO.title }}{% endif %}</title>
<link rel="stylesheet" href="{{ STATIC_URL }}css/base.min.css" />
{% if APP_NAME %}
    {% comment %} TODO: replace it to fully customizable something [1] {% endcomment %}
    <link rel="stylesheet" href="{{ STATIC_URL }}css/{{ APP_NAME }}.min.css" />
{% endif %}
<script src="{{ STATIC_URL }}js/modernizr.min.js"></script>
