-- models/reporting_data/rpt_data_tools_trends.sql
{{ config(materialized='incremental', schema='reporting_data') }}

SELECT 
    RANK() OVER (ORDER BY AAAA.tool_count DESC) AS rank
	, CASE 
	      WHEN AAAA.category IS NULL THEN 'Other'
		  ELSE AAAA.category
	  END AS category
	, AAAA.tool_name
	, AAAA.tool_count
	, AAAA.crawl_date
FROM(
	SELECT 
		BBB.category 
		, AAA.tool AS tool_name
		, COUNT(AAA.*) AS tool_count
		, AAA.crawl_date
	FROM (
		SELECT 
		    unnest(AA.tools) AS tool,
		    regexp_replace(lower(trim(unnest(AA.tools))), '[^a-z0-9+#]', '', 'g') AS tool_lower,
		    AA.crawl_date
		FROM {{ source('modeling_data', 'er_job') }} AA
		WHERE 
		    AA.crawl_date = '2024-05-20' 
	)AAA
	left join {{ source('modeling_data', 'er_tools') }}BBB on AAA.tool_lower = regexp_replace(lower(trim(BBB.tool_name)), '[^a-z0-9+#]', '', 'g')
	GROUP BY BBB.category, AAA.tool, AAA.crawl_date
)AAAA
ORDER BY AAAA.tool_count DESC