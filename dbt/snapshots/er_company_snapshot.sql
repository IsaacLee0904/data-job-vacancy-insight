{% snapshot er_company_snapshot %}  

{{
  config(
    target_database='job_vacancy_insight_datawarehouse',
    target_schema='modeling_data',
    strategy='check',
    unique_key="company_id",
    check_cols='all',
  )
}}

SELECT *
FROM {{ source('modeling_data', 'er_company') }}

{% endsnapshot %}