-- models/reporting_data/rpt_data_tools_trends.sql
{{ config(materialized='incremental', schema='reporting_data') }}

SELECT
    j.unique_id,
    t.tools
FROM {{ ref('er_job') }} AS j
CROSS JOIN LATERAL (
    SELECT
        t.tools
    FROM {{ ref('er_data_tools') }} AS t
    WHERE
        {{ regex_match('j.job_description', 't.tools') }} OR
        {{ regex_match('j.others', 't.tools') }}
) AS t

