-- models/training_data/train_user_recommendations.sql
{{ config(materialized='table', schema='training_data', unique_key='unique_id || crawl_date')}}

SELECT 
	AAA.unique_id 
	, AAA.data_role 
	, AAA.job_title 
	, BBB.company_name
	, AAA.salary 
	, AAA.job_description 
	, AAA.experience
	, AAA.tools 
	, AAA."others" 
	, AAA.url 
    , AAA.crawl_date
FROM {{ source('modeling_data', 'er_job') }}AAA
LEFT JOIN (SELECT * FROM {{ source('modeling_data', 'er_company') }}BB)BBB on AAA.company_id = BBB.company_id