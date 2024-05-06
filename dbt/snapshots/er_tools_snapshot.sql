{% snapshot er_tools_snapshot %}  

{{
  config(
    target_database='job_vacancy_insight_datawarehouse',
    target_schema='modeling_data',
    strategy='check',
    unique_key="tool_id",
    check_cols='all',
  )
}}

SELECT *
FROM {{ source('modeling_data', 'er_tools') }}

{% endsnapshot %}