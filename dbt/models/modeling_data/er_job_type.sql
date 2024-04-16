-- models/modeling_data/er_job_type.sql 
-- need to initialize with the first week 
{{ config(materialized='table', unique_key='job_type_id') }}

WITH current_week AS (
    SELECT UNNEST(job_type) AS job_type
    FROM {{ source('staging_data', 'job_listings_104') }}
    WHERE 1 = 1
        AND crawl_date = '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}'
        AND data_role IN ('Data Analyst', 'Data Scientist', 'Data Engineer', 'Machine Learning Engineer', 'Business Analyst', 'Data Architect', 'BI Engineer')
    GROUP BY job_type
),

previous_week AS (
    SELECT 
        job_type_id
        , job_type
    FROM {{ source('modeling_data', 'er_job_type') }} 
),

new_job_type AS (
    SELECT
        job_type
    FROM current_week
    WHERE job_type NOT IN (SELECT job_type FROM {{ source('modeling_data', 'er_job_type') }})
),

ranked_new_job_type AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY job_type) + (SELECT COALESCE(MAX(job_type_id), 0) FROM previous_week) AS job_type_id, 
        job_type
    FROM new_job_type
)

SELECT 
    job_type_id
    , job_type
FROM previous_week
UNION ALL
SELECT 
    job_type_id
    , job_type
FROM ranked_new_job_type