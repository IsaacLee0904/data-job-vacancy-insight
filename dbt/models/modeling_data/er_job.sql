-- models/modeling_data/er_job.sql
{{ config(materialized='incremental') }}

SELECT
    AA.data_role
    , AA.job_title
    , AA.salary
    , AA.job_description
    , AA.experience
    , AA.others
    , AA.url
    , AA.crawl_date
FROM {{ source('staging_data', 'job_listings_104') }} AA 
WHERE 1 = 1
    AND AA.crawl_date = '2024-04-08'
--  AND AA.crawl_date = '{{ dbt.date.current_date() }}'
    AND AA.data_role IN ('Data Analyst', 'Data Scientist', 'Data Engineer', 'Machine Learning Engineer', 'Business Analyst', 'Data Architect', 'BI Engineer')