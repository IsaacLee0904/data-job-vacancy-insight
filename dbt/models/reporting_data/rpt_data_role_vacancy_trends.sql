-- models/reporting_data/rpt_data_role_vacancy_trends.sql
{{ config(materialized='incremental', schema='reporting_data') }}

SELECT
    data_role
    , count(data_role) AS count
    , crawl_date 
WHERE crawl_date = '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}'
GROUP BY data_role, crawl_date 
ORDER BY count(data_role) DESC