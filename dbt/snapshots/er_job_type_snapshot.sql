{% snapshot er_job_type_snapshot %}  

{{
  config(
    target_database='job_vacancy_insight_datawarehouse',
    target_schema='modeling_data',
    strategy='check',
    unique_key="job_type_id",
    check_cols='all',
  )
}}

SELECT *
FROM {{ source('modeling_data', 'er_job_type') }}

{% endsnapshot %}