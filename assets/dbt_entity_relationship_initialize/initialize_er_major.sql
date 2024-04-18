SELECT 
	ROW_NUMBER() OVER (ORDER BY AAA.major) AS major_id
	, AAA.major
FROM(
	SELECT 
		UNNEST(AA.major_required) AS major
	FROM {{ source('staging_data', 'job_listings_104') }} AA
	WHERE 1 = 1
	    AND AA.crawl_date = '2024-04-01'
	    AND AA.data_role IN ('Data Analyst', 'Data Scientist', 'Data Engineer', 'Machine Learning Engineer', 'Business Analyst', 'Data Architect', 'BI Engineer')
)AAA
GROUP BY AAA.major 