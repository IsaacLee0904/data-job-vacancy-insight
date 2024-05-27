-- models/reporting_data/rpt_job_openings_metrics.sql
{{ config(materialized='incremental', schema='reporting_data', unique_key='crawl_date') }}

WITH previous_week AS (
    SELECT url
    FROM {{ source('modeling_data', 'er_job') }}
    WHERE crawl_date = '{{ get_last_monday() }}'
),
current_week AS (
    SELECT url
    FROM {{ source('modeling_data', 'er_job') }}
    WHERE crawl_date = '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}'
)
SELECT
    COUNT(current_week.url) AS total_openings
    , (SELECT COUNT(url) FROM previous_week WHERE url NOT IN (SELECT url FROM current_week)) AS closed_openings_count
    , (SELECT COUNT(url) FROM current_week WHERE url NOT IN (SELECT url FROM previous_week)) AS new_openings_count
    , COALESCE(
        (SELECT COUNT(url) FROM previous_week WHERE url NOT IN (SELECT url FROM current_week))::float / COUNT(current_week.url),
        0
    ) AS fill_rate
    , '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}' AS crawl_date
FROM current_week