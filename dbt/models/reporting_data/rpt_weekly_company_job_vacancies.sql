-- models/reporting_data/rpt_weekly_company_job_vacancies.sql
{{ config(materialized='incremental', schema='reporting_data', unique_key='company_name || crawl_date') }}

SELECT 
    RANK() OVER (ORDER BY AAA.opening_count DESC) AS rank
    , BBB.company_name
    , AAA.opening_count
    , AAA.crawl_date    
FROM (
    SELECT 
        AA.company_id
        , COUNT(AA.company_id) AS opening_count
        , AA.crawl_date
    FROM {{ source('modeling_data', 'er_job') }} AA
    WHERE AA.crawl_date = '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}'
    GROUP BY AA.company_id, AA.crawl_date
) AAA
LEFT JOIN modeling_data.er_company BBB ON AAA.company_id = BBB.company_id 
ORDER BY AAA.opening_count DESC


