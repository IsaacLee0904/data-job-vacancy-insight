{% macro get_last_monday() %}
    {% set today = modules.datetime.date.today() %}
    {% set weekday = today.weekday() %}  
    {% set days_since_monday = (weekday + 6) % 7 + 1 %}  
    {% set last_monday = (today - modules.datetime.timedelta(days=days_since_monday)).strftime('%Y-%m-%d') %}
    {{ return(last_monday) }}
{% endmacro %}
