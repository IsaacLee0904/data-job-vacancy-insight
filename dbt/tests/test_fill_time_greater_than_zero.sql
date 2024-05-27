-- tests/test_fill_time_greater_than_zero copy.sql

SELECT average_weeks_to_fill
FROM {{ ref('rpt_job_fill_time_statistics') }}
WHERE average_weeks_to_fill <= 0
