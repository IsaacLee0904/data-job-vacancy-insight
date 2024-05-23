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
- Dashboard
    - Design Dashboard with Figma (in-progress)
    - Data pipeline - Transfrom data in the data warehouse (reporting_data layer) for dashboard (in-progress)
        - Home page(**2024-05-22 to 2024-05-23**)
        - Skill page
        - Education page 
        - Geograph page

## Project Overview
The "Data-Job-Vacancy-Insight" project is designed to streamline the job searching process for data professionals. By aggregating and analyzing job listings from multiple sources, it offers personalized job recommendations and valuable market insights directly through a user-friendly Telegram bot interface.

## Features
- **Job Recommendations:** Tailored suggestions based on user's skills and preferences.
- **Market Insights:** Analysis of current job market trends within the data field.
- **User Profiles:** Customizable profiles that enhance job matching accuracy.
- **Automated Reports:** Regular updates and reports delivered through Telegram.

## Repository structure
```
├── Config
│   └── database_config.toml
├── Docker-compose.yml
├── Dockerfile
├── README.md
├── assets
│   ├── dbt_entity_relationship_initialize
│   │   ├── initialize_er_company.sql
│   │   ├── initialize_er_job_type.sql
│   │   ├── initialize_er_major.sql
│   │   └── initialize_er_tools.sql
│   └── entity_relationship_model
│       ├── job_vacancy_insight_datawarehouse_entity_relationship.png
│       └── job_vacancy_insight_datawarehouse_entity_relationship.sql
├── data
│   ├── backup
│   │   ├── jobs_20240401_065532.json
│   │   ├── jobs_20240408_135846.json
│   │   └── jobs_20240415_012649.json
│   ├── database
│   └── raw_data
├── dbt
│   ├── dbt_packages
│   ├── dbt_project.yml
│   ├── logs
│   │   └── dbt.log
│   ├── macros
│   │   └── er_function.sql
│   ├── models
│   │   ├── modeling_data
│   │   │   ├── er_company.sql
│   │   │   ├── er_company_location.sql
│   │   │   ├── er_degree.sql
│   │   │   ├── er_job.sql
│   │   │   ├── er_job_type.sql
│   │   │   ├── er_major.sql
│   │   │   └── er_tools.sql
│   │   ├── source_data
│   │   ├── sources.yml
│   │   └── staging_data
│   ├── packages.yml
│   ├── profiles.yml
│   ├── seeds
│   │   ├── er_county.csv
│   │   └── er_district.csv
│   ├── snapshots
│   └── target
├── docs
├── logs
│   ├── 104_crawler.log
│   ├── dbt.log
│   ├── graylog_checker.log
│   ├── load_raw_data.log
│   ├── test.log
│   └── transform_raw_data.log
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