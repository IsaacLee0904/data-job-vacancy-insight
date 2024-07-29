# Data-Job-Vacancy-Insight
A system that recommends data-centric jobs and provides insights, featuring a personalized job report service delivered through a Telegram bot.

## Authors 
- [@IsaacLee0904](https://github.com/IsaacLee0904)

## Timeline
- **2024-03-25:** Project workflow design
- **2024-03-26:** Set up development environment with Docker
- **2024-03-28 to 2024-03-31:** Development of 104 crawler
- **2024-03-31:** Database design (https://dbdiagram.io/d/job_vacancy_insight_datawarehouse_modeling-66209be403593b6b614a0bda)
- **2024-04-01 to 2024-04-02:** Data pipeline - Load raw data into the data warehouse (source_data layer)
- **2024-04-08 to 2024-04-09:** Data pipeline - Transform data in the data warehouse (staging_data layer)
- **2024-04-09 to 2024-04-10:** Set up DBT (Data Build Tool)
- **2024-04-12 to 2024-04-22:** Data pipeline - Transform data into the data warehouse (modeling_data layer) with dbt
    - ER model build up in modeling_data layer with dbt model feature
    - ER model tables data quality check setup with dbt test feature
    - Data warehouse modeling_data layer graph (http://localhost:80)
    - Data warehouse modeling_data layer change data capture(CDC) setup with dbt snapshot feature 
- Deploy with airflow 
    - Error message with telegram alert (**2024-05-20**)
    - Data pipeline (**2024-05-05**)
        - 104 crawler
        - Data pipeline - load raw data
        - Data pipeline - transform data
        - Data pipeline - ER modeling 
        - Data quality check 
        - Change data capture
- Dashboard (https://datawonderlust.onrender.com)
    - Create dashboard
        - Home page
            - Design Dashboard with Figma (**2024-05-21 to 2024-05-22**)
            - Data pipeline - Transfrom data in the data warehouse (reporting_data layer) for dashboard (**2024-05-22 to 2024-05-23**)
            - Dash page content setup include html and CSS (**2024-05-24 to 2024-06-11**)
            - Dashboard figure creating (**2024-06-11 to 2024-06-16**)
        - Stack page
            - Design Dashboard with Figma (**2024-06-18**)
            - Data pipeline - Transfrom data in the data warehouse (reporting_data layer) for dashboard(**2024-06-19**)
            - Dash page content setup include html and CSS (**2024-05-24 to 2024-06-11**)
            - Dashboard figure creating (**2024-06-22 to 2024-06-27**)
        - Education page 
            - Design Dashboard with Figma (**2024-06-29**)
            - Data pipeline - Transfrom data in the data warehouse (reporting_data layer) for dashboard(**2024-07-06**)
            - Dash page content setup include html and CSS (**2024-05-24 to 2024-06-11**)
            - Dashboard figure creating(**2024-07-07**)
        - Geograph page
            - Design Dashboard with Figma(**2024-07-08**)
            - Data pipeline - Transfrom data in the data warehouse (reporting_data layer) for dashboard (**2024-07-12**)
            - Dash page content setup include html and CSS (**2024-05-24 to 2024-06-11**)
            - Dashboard figure creating (**2024-07-12 to 2024-07-15**)
    - Deploy dashboard app into public web (**2024-07-15 to 2024-07-29**)

## Project Overview
The "Data-Job-Vacancy-Insight" project is designed to streamline the job searching process for data professionals. By aggregating and analyzing job listings from multiple sources, it offers personalized job recommendations and valuable market insights directly through a user-friendly Telegram bot interface.

## Features
- **Job Recommendations:** Tailored suggestions based on user's skills and preferences.
- **Market Insights:** Analysis of current job market trends within the data field.
    - deploy with render : https://datawonderlust.onrender.com
- **User Profiles:** Customizable profiles that enhance job matching accuracy.
- **Automated Reports:** Regular updates and reports delivered through Telegram.

## Repository structure
```
├── Docker-compose.yml
├── Dockerfile
├── README.md
├── airflow_dags
│   └── data_pipeline_dag.py
├── assets
│   ├── dbt_entity_relationship_initialize 
│   ├── entity_relationship_model
│   └── front_end
│       ├── assets
│       │   ├── images
│       │   └── vectors
│       ├── css
│       └── html
├── config
│   └── database_config.toml
├── data
│   ├── backup
│   ├── database
│   └── raw_data
├── dbt
│   ├── dbt_project.yml
│   ├── logs
│   ├── macros
│   │   ├── er_function.sql
│   │   ├── get_custom_schema.sql
│   │   ├── get_last_monday.sql
│   │   └── regex_match.sql
│   ├── models
│   │   ├── modeling_data
│   │   │   ├── er_company.sql
│   │   │   ├── er_company_location.sql
│   │   │   ├── er_degree.sql
│   │   │   ├── er_job.sql
│   │   │   ├── er_job_type.sql
│   │   │   └── er_major.sql
│   │   ├── reporting_data
│   │   │   ├── rpt_data_role_vacancy_trends.sql
│   │   │   ├── rpt_data_tools_trends.sql
│   │   │   ├── rpt_job_fill_time_statistics.sql
│   │   │   ├── rpt_job_openings_geograph.sql
│   │   │   ├── rpt_job_openings_metrics.sql
│   │   │   └── rpt_weekly_company_job_vacancies.sql
│   │   ├── staging_data
│   │   ├── source_data
│   │   ├── sources.yml
│   │   └── schema.yml
│   ├── profiles.yml
│   ├── seeds
│   │   ├── er_county.csv
│   │   ├── er_district.csv
│   │   └── er_tools.csv
│   ├── snapshots
│   └── tests
│       ├── er_job_crawl_date.sql
│       ├── seeds_generic_test.yml
│       ├── test_data_role_count_greater_than_zero.sql
│       ├── test_data_tools_count_greater_than_zero.sql
│       ├── test_openings_by_company_greater_than_zero.sql
│       ├── test_openings_by_geograph_greater_than_zero.sql
│       └── test_openings_metrics.sql
├── docs
│   └── dbt.md
├── main.py
├── model
├── references
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── buildup_src
│   │   ├── database_connection_checker.py
│   │   ├── graylog_checker.py
│   │   └── package_checker.py
│   ├── crawler_src
│   │   └── 104_crawler.py
│   ├── dashboard_src
│   │   └── dashboard_app.py
│   └── data_processing_src
│       ├── load_raw_data.py
│       └── transform_raw_data.py
└── utils
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-38.pyc
    │   ├── crawler_utils.cpython-38.pyc
    │   ├── database_utils.cpython-38.pyc
    │   ├── etl_utils.cpython-38.pyc
    │   └── log_utils.cpython-38.pyc
    ├── crawler_utils.py
    ├── database_utils.py
    ├── etl_utils.py
    └── log_utils.py
```