{{ config(materialized='table', unique_key='company_id') }}

SELECT 
	AAAA.company_id
	, AAAA.company_name
	, AAAA.county_id
	, CASE 
	      WHEN AAAA.district_id IS NULL THEN AAAA.county_id
	      ELSE AAAA.district_id
	END AS district_id	
FROM(
	SELECT 
		BBB.company_id
		, AAA.company_name
		, CCC.county_id
		, DDD.district_id
	FROM {{ source('staging_data', 'job_listings_104') }} AAA
	LEFT JOIN(
		SELECT BB.* 
		FROM {{ ref('er_company') }} BB
	)BBB ON 1 = 1
		AND AAA.company_name = BBB.company_name
	LEFT JOIN(
		SELECT CC.*
		FROM {{ ref('er_county') }} CC
	)CCC ON 1 = 1
		AND AAA.county = CCC.county_name_ch
	LEFT JOIN(
		SELECT DD.*
		FROM {{ ref('er_district') }} DD 
	)DDD ON 1 = 1
		AND AAA.location = DDD.district_name_ch
	WHERE 1 = 1
		AND AAA.data_role IN ('Data Analyst', 'Data Scientist', 'Data Engineer', 'Machine Learning Engineer', 'Business Analyst', 'Data Architect', 'BI Engineer')
	GROUP BY BBB.company_id, AAA.company_name, CCC.county_id, DDD.district_id
)AAAA