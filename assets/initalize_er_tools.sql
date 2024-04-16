SELECT 
	ROW_NUMBER() OVER (ORDER BY AAA.tool) AS tool_id
	, AAA.tool
FROM(
	SELECT 
		UNNEST(AA.tools) AS tool
	FROM {{ source('staging_data', 'job_listings_104') }} AA
	WHERE 1 = 1
	    AND AA.crawl_date = '2024-04-01'
	    AND AA.data_role IN ('Data Analyst', 'Data Scientist', 'Data Engineer', 'Machine Learning Engineer', 'Business Analyst', 'Data Architect', 'BI Engineer')
)AAA
GROUP BY AAA.tool   