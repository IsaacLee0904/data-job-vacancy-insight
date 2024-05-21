-- models/reporting_data/rpt_job_average_fill_time.sql
{{ config(materialized='incremental', schema='reporting_data') }}

WITH job_url_appearance AS (
    SELECT
        url,
        MIN(crawl_date) AS first_appearance,
        MAX(crawl_date) AS last_appearance
    FROM
         {{ source('modeling_data', 'er_job') }}
    GROUP BY
        url
),
job_durations AS(
    SELECT
        url,
        first_appearance,
        last_appearance,
        (last_appearance - first_appearance) / 7 AS duration_weeks
    FROM
        job_url_appearance
    WHERE
           last_appearance != '2024-05-20'          
)
SELECT
    '2024-05-20' AS current_date,
    AVG(duration_weeks) AS average_weeks_to_fill    
FROM
    job_durations