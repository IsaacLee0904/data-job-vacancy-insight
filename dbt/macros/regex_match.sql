{% macro regex_match(field, pattern) %}
  {{ field }} ~* {{ "'" ~ pattern ~ "'" }}
{% endmacro %}
