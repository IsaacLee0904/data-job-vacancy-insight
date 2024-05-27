-- tests/test_data_tools_count_greater_than_zero.sql

SELECT tool_count
FROM {{ ref('rpt_data_tools_trends') }}
WHERE tool_count <= 0
