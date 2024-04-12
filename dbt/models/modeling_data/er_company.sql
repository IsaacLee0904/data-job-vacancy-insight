-- models/modeling_data/er_company.sql 
{{ config(materialized='table', unique_key='company_id') }}


SELECT DISTINCT company_name
FROM {{ source('staging_data', 'job_listings_104') }}

