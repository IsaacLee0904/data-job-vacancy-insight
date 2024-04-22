{% snapshot er_major_snapshot %}  

{{
  config(
    target_database='job_vacancy_insight_datawarehouse',
    target_schema='modeling_data',
    strategy='check',
    unique_key="major_id",
    check_cols=['status', 'is_cancelled'],
  )
}}

SELECT *
FROM {{ source('modeling_data', 'er_major') }}

{% endsnapshot %}