-- models/reporting_data/rpt_job_fill_time_statistics.sql
{{ config(materialized='incremental', schema='reporting_data', unique_key='current_date') }}

WITH job_url_appearance AS (
    SELECT
        url
        , MIN(crawl_date) AS first_appearance
        , MAX(crawl_date) AS last_appearance
    FROM {{ source('modeling_data', 'er_job') }}
    WHERE crawl_date <= '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}'
    GROUP BY url
),
job_durations AS(
    SELECT
        url
        , first_appearance
        , last_appearance
        , (last_appearance - first_appearance) / 7 AS duration_weeks
    FROM job_url_appearance
    WHERE last_appearance != '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}'         
)
SELECT
    AVG(duration_weeks) AS average_weeks_to_fill
    , '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}' AS current_date 
FROM
    job_durations