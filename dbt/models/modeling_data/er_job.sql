-- models/modeling_data/er_job.sql 
{{ config(materialized='incremental', unique_key='unique_id') }}

SELECT
    {{ generate_unique_id('AA.id', 'AA.crawl_date') }}
    , AA.data_role
    , AA.job_title
    , AA.salary
    , AA.job_description
    , AA.experience
    , AA.others
    , AA.url
    , AA.crawl_date
FROM {{ source('staging_data', 'job_listings_104') }} AA 
WHERE 1 = 1
    AND AA.crawl_date = '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}'
    AND AA.data_role IN ('Data Analyst', 'Data Scientist', 'Data Engineer', 'Machine Learning Engineer', 'Business Analyst', 'Data Architect', 'BI Engineer')


