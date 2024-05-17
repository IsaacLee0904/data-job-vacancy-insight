-- models/reporting_data/rpt_data_role.sql
{{ config(materialized='table', schema='reporting_data') }}

SELECT
    data_role
    , count(data_role) AS count
    , crawl_date 
FROM {{ source('modeling_data', 'er_job') }}
WHERE crawl_date = '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}'
GROUP BY data_role, crawl_date 
ORDER BY count(data_role) DESC