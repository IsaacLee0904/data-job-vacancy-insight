SELECT
    ROW_NUMBER() OVER (ORDER BY company_name) AS company_id
    , company_name
FROM {{ source('staging_data', 'job_listings_104') }}
WHERE 1 = 1
    AND crawl_date = '2024-04-01'
    AND data_role IN ('Data Analyst', 'Data Scientist', 'Data Engineer', 'Machine Learning Engineer', 'Business Analyst', 'Data Architect', 'BI Engineer')
GROUP BY company_name