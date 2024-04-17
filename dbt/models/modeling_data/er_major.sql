-- models/modeling_data/er_major.sql 
-- need to initialize with the first week 
 {{ config(materialized='table', unique_key='major_id') }}

WITH current_week AS (
    SELECT UNNEST(major_required) AS major
    FROM {{ source('staging_data', 'job_listings_104') }}
    WHERE 1 = 1
        AND crawl_date = '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}'
        AND data_role IN ('Data Analyst', 'Data Scientist', 'Data Engineer', 'Machine Learning Engineer', 'Business Analyst', 'Data Architect', 'BI Engineer')
    GROUP BY major
),

previous_week AS (
    SELECT 
        major_id
        , major
    FROM {{ source('modeling_data', 'er_major') }} 
),

new_majors AS (
    SELECT
        major
    FROM current_week
    WHERE major NOT IN (SELECT major FROM {{ source('modeling_data', 'er_major') }})
),

ranked_new_majors AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY major) + (SELECT COALESCE(MAX(major_id), 0) FROM previous_week) AS major_id, 
        major
    FROM new_majors
)

SELECT 
    major_id
    , major
FROM previous_week
UNION ALL
SELECT 
    major_id
    , major
FROM ranked_new_majors  