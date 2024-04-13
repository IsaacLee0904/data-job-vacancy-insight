{{ config(materialized='table', unique_key='company_id') }}

select 
	BBB.company_id
	, AAA.company_name
	, CCC.county_id
	, DDD.district_id
from staging_data.job_listings_104 AAA
left join(
	select BB.* 
	from modeling_data.er_company BB
)BBB on 1 = 1
	and AAA.company_name = BBB.company_name
left join(
	select CC.*
	from modeling_data.er_county CC
)CCC on 1 = 1
	and AAA.county = CCC.county_name_ch
left join(
	select DD.*
	from modeling_data.er_district DD 
)DDD on 1 = 1
	and AAA.location = DDD.district_name_ch
where 1 = 1
	and AAA.data_role in ('Data Analyst', 'Data Scientist', 'Data Engineer', 'Machine Learning Engineer', 'Business Analyst', 'Data Architect', 'BI Engineer')
group by BBB.company_id, AAA.company_name, CCC.county_id, DDD.district_id