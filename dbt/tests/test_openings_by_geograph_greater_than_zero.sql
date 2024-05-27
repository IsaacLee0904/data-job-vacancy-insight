-- tests/test_openings_by_geograph_greater_than_zero.sql

SELECT openings_count
FROM {{ ref('rpt_job_openings_geograph') }}
WHERE openings_count <= 0
