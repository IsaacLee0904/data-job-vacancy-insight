-- tests/test_data_role_count_greater_than_zero.sql

SELECT count
FROM {{ ref('rpt_data_role_vacancy_trends') }}
WHERE count <= 0
