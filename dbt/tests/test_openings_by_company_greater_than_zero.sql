-- tests/test_openings_by_company_greater_than_zero.sql

SELECT opening_count
FROM {{ ref('rpt_weekly_company_job_vacancies') }}
WHERE opening_count <= 0 
