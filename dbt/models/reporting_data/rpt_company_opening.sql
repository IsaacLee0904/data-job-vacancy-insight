-- models/reporting_data/rpt_company_opening.sql
{{ config(materialized='incremental', schema='reporting_data') }}

SELECT 
    BBB.company_name,
    AAA.opening_count,
    AAA.crawl_date,
    RANK() OVER (ORDER BY AAA.opening_count DESC) AS rank
FROM (
    SELECT 
        AA.company_id,
        COUNT(AA.company_id) AS opening_count,
        AA.crawl_date
    FROM 
        modeling_data.er_job AA
    WHERE 
        AA.crawl_date = '2024-05-13'
    GROUP BY 
        AA.company_id, AA.crawl_date
) AAA
LEFT JOIN 
    modeling_data.er_company BBB 
ON 
    AAA.company_id = BBB.company_id 
ORDER BY 
    AAA.opening_count DESC


