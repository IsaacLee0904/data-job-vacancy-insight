{% SNAPSHOT er_company_location_snapshot %}  

{{
  config(
    target_database='job_vacancy_insight_datawarehouse',
    target_schema='modeling_data',
    strategy='check',
    unique_key="company_id||'-'||district_id",
    check_cols=['status', 'is_cancelled'],
  )
}}

SELECT 
  "company_id||'-'||district_id"
  , *
FROM {{ source('modeling_data', 'er_company_location') }}

{% endsnapshot %}