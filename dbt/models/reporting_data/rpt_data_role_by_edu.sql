-- models/reporting_data/rpt_data_role_by_edu.sql
{{ config(materialized='incremental', schema='reporting_data', unique_key='data_role || degree || crawl_date')}}

SELECT
	CASE
		WHEN AAA.data_role = 'Machine Learning Engineer' THEN 'MLE'
        ELSE AAA.data_role
    END AS data_role
    , CASE 
    	WHEN BBB.degree = 'PhD' THEN 'PhD'
    	WHEN BBB.degree = 'Master Degree' THEN 'Master'
    	WHEN BBB.degree = 'Bachelor Degree' THEN 'Bachelor'
    	WHEN BBB.degree = 'College Degree' THEN 'College Degree'
    	WHEN BBB.degree = 'High School' THEN 'High School'
    	WHEN BBB.degree = 'Others' THEN 'Others'
    END degree
    , COUNT(*) AS count
    , AAA.crawl_date
FROM (
    SELECT 
        AA.data_role,
        unnest(AA."degree") AS degree,
        AA.crawl_date
    FROM modeling_data.er_job AA
    WHERE AA.crawl_date = '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}'
) AAA
LEFT JOIN (
    SELECT BB.degree_id, BB.degree
    FROM modeling_data.er_degree BB
) BBB
ON AAA."degree" = BBB.degree_id
GROUP BY
    AAA.data_role,
    BBB.degree,
    AAA.crawl_date
ORDER BY
    AAA.data_role,
    BBB.degree