-- models/reporting_data/rpt_data_tools_by_data_role.sql
{{ config(materialized='incremental', schema='reporting_data', unique_key='data_role || tool_name || crawl_date') }}

WITH listing_table AS (
	SELECT DISTINCT
	    BB.data_role,
	    AA.category,
	    AA.tool_name,
	    BB.crawl_date
	FROM modeling_data.er_tools AA
	CROSS JOIN (SELECT DISTINCT data_role, crawl_date FROM modeling_data.er_job WHERE crawl_date = '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}') BB
)
SELECT 
	listing_table.data_role
	, listing_table.category
	, listing_table.tool_name 
	, CASE 
	  	WHEN counting_table.count IS NOT NULL THEN counting_table.count
	  	ELSE 0 
	END AS count
	, listing_table.crawl_date
FROM listing_table
LEFT JOIN(
	SELECT
		AAA.data_role
		, AAA.tool
		, AAA.tool_lower
		, COUNT(AAA.*) AS count
		, AAA.crawl_date
	FROM(
		SELECT 
			AA.data_role, 
			unnest(AA.tools) AS tool,
		    regexp_replace(lower(trim(unnest(AA.tools))), '[^a-z0-9+#]', '', 'g') AS tool_lower,
		    AA.crawl_date
		FROM modeling_data.er_job AA
		WHERE AA.crawl_date = '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}'
	) AAA
	GROUP BY AAA.data_role, AAA.tool, AAA.tool_lower, AAA.crawl_date
) counting_table
ON 1 = 1
	AND counting_table.tool_lower = regexp_replace(lower(trim(listing_table.tool_name)), '[^a-z0-9+#]', '', 'g')
	AND counting_table.data_role = listing_table.data_role