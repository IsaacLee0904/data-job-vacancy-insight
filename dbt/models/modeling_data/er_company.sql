-- models/modeling_data/er_company.sql 
-- need to initialize with the first week 
{{ config(materialized='table', unique_key='company_id') }}

WITH current_week AS (
    SELECT company_name
    FROM {{ source('staging_data', 'job_listings_104') }}
    WHERE 1 = 1
        AND crawl_date = '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}'
        AND data_role IN ('Data Analyst', 'Data Scientist', 'Data Engineer', 'Machine Learning Engineer', 'Business Analyst', 'Data Architect', 'BI Engineer')
    GROUP BY company_name
),

previous_week AS (
    SELECT 
        company_id
        , company_name
    FROM {{ source('modeling_data', 'er_company') }} 
),

new_companies AS (
    SELECT
        company_name
    FROM current_week
    WHERE company_name NOT IN (SELECT company_name FROM {{ source('modeling_data', 'er_company') }})
),

ranked_new_companies AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY company_name) + (SELECT COALESCE(MAX(company_id), 0) FROM previous_week) AS company_id, 
        company_name
    FROM new_companies
)

SELECT 
    company_id
    , company_name
FROM previous_week
UNION ALL
SELECT 
    company_id
    , company_name
FROM ranked_new_companies



