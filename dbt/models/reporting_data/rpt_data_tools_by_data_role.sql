-- models/reporting_data/rpt_data_tools_by_data_role.sql
{{ config(materialized='incremental', schema='reporting_data', unique_key='data_role || tool_name') }}

SELECT 
	AAA.data_role
	, BBB.category 
	, AAA.tool AS tool_name
	, COUNT(AAA.*) AS tool_count
	, AAA.crawl_date
FROM(
	SELECT 
		data_role, 
		unnest(AA.tools) AS tool,
	    regexp_replace(lower(trim(unnest(AA.tools))), '[^a-z0-9+#]', '', 'g') AS tool_lower,
	    AA.crawl_date
	FROM {{ source('modeling_data', 'er_job') }} AA
	WHERE 
	    AA.crawl_date = '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}'
)AAA
LEFT JOIN {{ source('modeling_data', 'er_tools') }} BBB ON AAA.tool_lower = regexp_replace(lower(trim(BBB.tool_name)), '[^a-z0-9+#]', '', 'g')
GROUP BY BBB.category, AAA.tool, AAA.crawl_date, AAA.data_role
ORDER BY AAA.tool, COUNT(AAA.*) DESC