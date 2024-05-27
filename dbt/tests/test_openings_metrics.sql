-- tests/test_openings_metrics.sql

SELECT total_openings, closed_openings_count, new_openings_count, fill_rate
FROM {{ ref('rpt_job_openings_metrics') }}
WHERE total_openings <= 0 AND closed_openings_count <= 0 AND new_openings_count <= 0 AND fill_rate BETWEEN 0 AND 1
