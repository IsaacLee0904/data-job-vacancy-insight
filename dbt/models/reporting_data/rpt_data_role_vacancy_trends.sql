-- models/reporting_data/rpt_data_role_vacancy_trends.sql
{{ config(materialized='incremental', schema='reporting_data', unique_key='data_role || crawl_date') }}

SELECT
    data_role
    , count(data_role) AS count
    , crawl_date 
FROM {{ source('modeling_data', 'er_job') }}
WHERE crawl_date = '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}'
GROUP BY data_role, crawl_date 
ORDER BY count(data_role) DESC