-- openings_statistics_metrics
SELECT 
	AAAA.total_openings
	, COALESCE(((AAAA.total_openings - AAAA.prev_total_openings) / NULLIF(CAST(AAAA.prev_total_openings AS FLOAT), 0)) * 100.0, 0) AS total_openings_change_pct
	, AAAA.closed_openings_count
	, COALESCE(((AAAA.closed_openings_count - AAAA.prev_closed_openings_count) / NULLIF(CAST(AAAA.prev_closed_openings_count AS FLOAT), 0)) * 100.0, 0) AS closed_openings_change_pct
	, AAAA.new_openings_count
	, COALESCE(((AAAA.new_openings_count - AAAA.prev_new_openings_count) / NULLIF(CAST(AAAA.prev_new_openings_count AS FLOAT), 0)) * 100.0, 0) AS new_openings_change_pct
	, AAAA.fill_rate
	, COALESCE(((AAAA.fill_rate - AAAA.prev_fill_rate) / NULLIF(CAST(AAAA.prev_fill_rate AS FLOAT), 0)) * 100.0, 0) AS fill_rate_change_pct
	, AAAA.average_weeks_to_fill
	, COALESCE(((AAAA.average_weeks_to_fill - AAAA.prev_average_weeks_to_fill) / NULLIF(CAST(AAAA.prev_average_weeks_to_fill AS FLOAT), 0)) * 100.0, 0) AS average_weeks_to_fill_change_pct
	, AAAA.crawl_date
FROM(
	SELECT 
		AAA.total_openings
		, LEAD(AAA.total_openings) OVER (ORDER BY AAA.crawl_date DESC) AS prev_total_openings
		, AAA.closed_openings_count
		, LEAD(AAA.closed_openings_count) OVER (ORDER BY AAA.crawl_date DESC) AS prev_closed_openings_count
		, AAA.new_openings_count
		, LEAD(AAA.new_openings_count) OVER (ORDER BY AAA.crawl_date DESC) AS prev_new_openings_count
		, AAA.fill_rate
		, LEAD(AAA.fill_rate) OVER (ORDER BY AAA.crawl_date DESC) AS prev_fill_rate
		, BBB.average_weeks_to_fill 
		, LEAD(BBB.average_weeks_to_fill) OVER (ORDER BY AAA.crawl_date DESC) AS prev_average_weeks_to_fill 
		, AAA.crawl_date
	FROM reporting_data.rpt_job_openings_metrics AAA
	LEFT JOIN (
		SELECT BBB.*
		FROM reporting_data.rpt_job_fill_time_statistics BBB
		WHERE BBB.current_date BETWEEN TO_CHAR(CAST('2024-05-27' AS date) - INTERVAL '7 days', 'YYYY-MM-DD') AND '2024-05-27'   
	) BBB ON AAA.crawl_date = BBB.current_date
	WHERE AAA.crawl_date BETWEEN TO_CHAR(CAST('2024-05-27' AS date) - INTERVAL '7 days', 'YYYY-MM-DD') AND '2024-05-27'
	ORDER BY AAA.crawl_date DESC
)AAAA
WHERE AAAA.crawl_date = '2024-05-27';