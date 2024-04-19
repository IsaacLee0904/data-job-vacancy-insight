-- models/modeling_data/er_tools.sql
{{ config(materialized='table', unique_key='tool_id') }}

SELECT AAAA.*
FROM(
	SELECT 
		CASE 
			WHEN AAA.degree = '博士' THEN 1 
			WHEN AAA.degree IN ('碩士以上', '碩士') THEN 2
			WHEN AAA.degree in ('大學以上', '大學') THEN 3
			WHEN AAA.degree in ('專科以上', '專科') THEN 4
			WHEN AAA.degree in ('高中以上', '高中') THEN 5
			ELSE 6
	 	END AS degree_id
	 	, CASE 
			  WHEN AAA.degree = '博士' THEN 'PhD'
			  WHEN AAA.degree IN ('碩士以上', '碩士') THEN 'Master Degree'
			  WHEN AAA.degree in ('大學以上', '大學') THEN 'Bachelor Degree'
			  WHEN AAA.degree in ('專科以上', '專科') THEN 'College Degree'
			  WHEN AAA.degree in ('高中以上', '高中') THEN 'High School'
			  else 'Others'
	 	  END AS degree
	FROM(
		SELECT 
			unnest(AA.degree_required) AS degree
		FROM {{ source('staging_data', 'job_listings_104') }} AA
		WHERE 1 = 1
		    AND AA.data_role IN ('Data Analyst', 'Data Scientist', 'Data Engineer', 'Machine Learning Engineer', 'Business Analyst', 'Data Architect', 'BI Engineer')
		GROUP BY degree     
	)AAA
	ORDER BY degree_id
)AAAA
GROUP BY AAAA.degree_id, AAAA.degree
    