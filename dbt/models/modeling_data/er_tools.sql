-- models/modeling_data/er_tools.sql 
-- need to initialize with the first week 
{{ config(materialized='table', unique_key='tool_id') }}

WITH current_week AS (
    SELECT UNNEST(tools) AS tool
    FROM {{ source('staging_data', 'job_listings_104') }}
    WHERE 1 = 1
        AND crawl_date = '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}'
        AND data_role IN ('Data Analyst', 'Data Scientist', 'Data Engineer', 'Machine Learning Engineer', 'Business Analyst', 'Data Architect', 'BI Engineer')
    GROUP BY tool
),

previous_week AS (
    SELECT 
        tool_id
        , tool
    FROM {{ source('modeling_data', 'er_tools') }} 
),

new_tools AS (
    SELECT
        tool
    FROM current_week
    WHERE tool NOT IN (SELECT tool FROM {{ source('modeling_data', 'er_tools') }})
),

ranked_new_tools AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY tool) + (SELECT COALESCE(MAX(tool_id), 0) FROM previous_week) AS tool_id, 
        tool
    FROM new_tools
)

SELECT 
    tool_id
    , tool
FROM previous_week
UNION ALL
SELECT 
    tool_id
    , tool
FROM ranked_new_tools  