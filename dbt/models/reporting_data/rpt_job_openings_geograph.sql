WITH job_with_company_location AS (
    SELECT 
        AAA.unique_id,
        AAA.company_id,
        BBB.company_name, 
        CCC.county_id,
        CCC.district_id
    FROM modeling_data.er_job AAA
    LEFT JOIN modeling_data.er_company BBB ON AAA.company_id = BBB.company_id
    LEFT JOIN modeling_data.er_company_location CCC ON AAA.company_id = CCC.company_id
    WHERE AAA.crawl_date = '2024-04-01'    
),
county_job_counts AS (
    SELECT 
        J.company_id,
        J.county_id,
        J.district_id,
        COUNT(*) AS job_count
    FROM job_with_company_location J
    GROUP BY J.company_id, J.county_id, J.district_id
),
ranked_counties AS (
    SELECT 
        C.*,
        RANK() OVER (PARTITION BY C.company_id ORDER BY C.job_count DESC) AS rank
    FROM county_job_counts C
)
SELECT 
    E.county_name_eng,
    D.district_name_eng,
    R.job_count
FROM ranked_counties R
LEFT JOIN modeling_data.er_county E ON R.county_id = E.county_id
LEFT JOIN modeling_data.er_district D ON R.district_id = D.district_id
WHERE R.rank = 1;

select count(*)
from modeling_data.er_job ej 
where crawl_date = '2024-04-01'