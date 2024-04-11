{% macro generate_unique_id(id_field, date_field) %}
    CAST({{ id_field }} AS VARCHAR) || '_' || {{ date_field }} AS combined_id
{% endmacro %}