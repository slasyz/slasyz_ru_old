<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{{ title }}{% if APP_INFO.title %} - {{ APP_INFO.title }}{% endif %}</title>
<link rel="stylesheet" href="{{ STATIC_URL }}foundation/css/foundation.min.css" />
<link rel="stylesheet" href="{{ STATIC_URL }}base.css" />
{% if APP_NAME %}
    <link rel="stylesheet" href="{{ STATIC_URL }}{{ APP_NAME }}.css" />
{% endif %}
<script src="{{ STATIC_URL }}foundation/js/vendor/modernizr.js"></script>
