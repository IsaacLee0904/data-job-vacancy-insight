-- models/modeling_data/er_job.sql 
{{ config(materialized='incremental', unique_key='unique_id') }}

WITH unnset_data AS(
    SELECT 
        AAAA.id 
        , AAAA.data_role 
        , AAAA.job_title 
        , BBBB.company_id
        , AAAA.salary 
        , AAAA.job_description 
        , CCCC.job_type_id
        , DDDD.degree_id
        , EEEE.major_id
        , AAAA.experience
        , FFFF.tool_name AS tool
        , AAAA.others
        , AAAA.url
        , AAAA.crawl_date
    FROM(
        SELECT
            AAA.id 
            , AAA.data_role 
            , AAA.job_title 
            , AAA.company_name
            , AAA.salary 
            , AAA.job_description 
            , AAA.job_type
            , CASE 
                WHEN AAA.degree = '博士' THEN 'PhD'
                WHEN AAA.degree IN ('碩士以上', '碩士') THEN 'Master Degree'
                WHEN AAA.degree IN ('大學以上', '大學') THEN 'Bachelor Degree'
                WHEN AAA.degree IN ('專科以上', '專科') THEN 'College Degree'
                WHEN AAA.degree IN ('高中以上', '高中') THEN 'High School'
            ELSE 'Others' END AS degree
            , AAA.major
            , AAA.experience
            , AAA.tool
            , AAA.others
            , AAA.url
            , AAA.crawl_date
        FROM(
            SELECT 
                AA.id 
                , AA.data_role 
                , AA.job_title 
                , AA.company_name
                , AA.salary 
                , AA.job_description 
                , UNNEST(AA.job_type) AS job_type
                , UNNEST(AA.degree_required) AS degree
                , UNNEST(AA.major_required) AS major
                , AA.experience
                , UNNEST(AA.tools) AS tool
                , AA.others
                , AA.url
                , AA.crawl_date
            FROM {{ source('staging_data', 'job_listings_104') }} AA 
            )AAA
        )AAAA
    LEFT JOIN(
        SELECT BB.*
        FROM {{ source('modeling_data', 'er_company') }} BB 
    )BBBB ON 1 = 1
        AND AAAA.company_name = BBBB.company_name
    LEFT JOIN(
        SELECT CC.*
        FROM  {{ source('modeling_data', 'er_job_type') }} CC 
    )CCCC ON 1 = 1
        AND AAAA.job_type = CCCC.job_type
    LEFT JOIN(
        SELECT DD.*
        FROM {{ source('modeling_data', 'er_degree') }} DD 
    )DDDD ON 1 = 1
        AND AAAA.degree = DDDD.degree
    LEFT JOIN(
        SELECT EE.*
        FROM {{ source('modeling_data', 'er_major') }} EE 
    )EEEE ON 1 = 1
        AND AAAA.major = EEEE.major
    LEFT JOIN(
        SELECT FF.*
        FROM {{ source('modeling_data', 'er_tools') }} FF 
    )FFFF ON 1 = 1
        AND AAAA.tool = FFFF.tool_name
    WHERE 1 = 1
        AND AAAA.crawl_date = '{{modules.datetime.date.today().strftime('%Y-%m-%d')}}'
        AND AAAA.data_role IN ('Data Analyst', 'Data Scientist', 'Data Engineer', 'Machine Learning Engineer', 'Business Analyst', 'Data Architect', 'BI Engineer')
    ORDER BY AAAA.id
)
SELECT 
    {{ generate_unique_id('id', 'crawl_date') }}
    , data_role
    , job_title
    , company_id
    , salary
    , job_description
    , array_agg(DISTINCT job_type_id) FILTER (WHERE job_type_id IS NOT NULL) AS job_types
    , array_agg(DISTINCT degree_id) FILTER (WHERE degree_id IS NOT NULL) AS degree
    , array_agg(DISTINCT major_id) FILTER (WHERE major_id IS NOT NULL) AS majors
    , experience
    , array_agg(DISTINCT tool) FILTER (WHERE tool IS NOT NULL) AS tools
    , others
    , url
    , crawl_date
FROM unnset_data
GROUP BY id, data_role, job_title, company_id, salary, job_description, experience, others, url, crawl_date