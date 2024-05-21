-- models/reporting_data/rpt_job_opening_trends.sql
{{ config(materialized='incremental', schema='reporting_data') }}

WITH previous_week AS (
    SELECT
        url
    FROM
         {{ source('modeling_data', 'er_job') }}
    WHERE
        crawl_date = '2024-05-13'
),
current_week AS (
    SELECT
        url
    FROM
         {{ source('modeling_data', 'er_job') }}
    WHERE
        crawl_date = '2024-05-20'
)
SELECT
    '2024-05-20' AS crawl_date,
    COUNT(current_week.url) AS total_openings,
    (SELECT COUNT(url) FROM previous_week WHERE url NOT IN (SELECT url FROM current_week)) AS closed_openings_count,
    (SELECT COUNT(url) FROM current_week WHERE url NOT IN (SELECT url FROM previous_week)) AS new_openings_count,
    COALESCE(
        (SELECT COUNT(url) FROM previous_week WHERE url NOT IN (SELECT url FROM current_week))::float / COUNT(current_week.url),
        0
    ) AS fill_rate
FROM
    current_week