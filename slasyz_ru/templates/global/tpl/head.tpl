<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{{ title }}{% if APP_INFO.title %} - {{ APP_INFO.title }}{% endif %}</title>
<link rel="stylesheet" href="{{ STATIC_URL }}css/base.min.css" />
{% if APP_NAME %}
    <link rel="stylesheet" href="{{ STATIC_URL }}css/{{ APP_NAME }}.min.css" />
{% endif %}
<script src="{{ STATIC_URL }}js/modernizr.min.js"></script>
