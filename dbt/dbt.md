# dbt Doc.
## Overview
A project-specific dbt for Data-Job-Vacancy-Insight.
This dbt project is designed to transform raw data in datawarehouse staging_data into modeling_data and build up an ER model.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Models and Seeds](#models-and-seeds)
- [References](#references)

## Installation

### Step 1: Install dbt
Install dbt using Docker by adding this to your Dockerfile:

```bash
dbt-postgres == 1.3
```

### Step 2: Configure Database Connection
Edit `profiles.yml` file to configure the database connection settings:

```yaml
data_job_vacancy_insight:
    target: dev
    outputs:
        dev:
        type: postgres
        threads: 1
        host: datawarehouse  
        port: 5432
        user: IsaacLee
        pass: job_vacancy_insight
        dbname: job_vacancy_insight_datawarehouse 
        schema: modeling_data  

        prod:
        type: postgres
        threads: 1
        host: datawarehouse  
        port: 5432
        user: IsaacLee
        pass: job_vacancy_insight
        dbname: job_vacancy_insight_datawarehouse
```
### Step 3: Initialize dbt Project
Create `dbt_project.yml` and initialize dbt project:

```bash
dbt init
```

### Step 4: Install dbt Packages

Navigate to your dbt directory and install required packages:
```bash
cd dbt 
dbt deps
```

## Usage

### Build dbt Models
Create and edit models within the models directory:

```bash
# To build all models
dbt run 

# To build a specific model
dbt run -s er_company_location.sql
```

### Seed Data Management
Manage your seed data through dbt:

```bash
# Load all seeds
dbt seed 

# Load a specific seed
dbt seed -s er_county.csv
```

### Test
#### Generic Test
Generic tests in dbt are predefined tests applied to your models, such as `unique`, `not_null`, and `relationships`. These tests help to validate that your data meets basic expectations like uniqueness, presence of values, and referential integrity between tables. You can apply these tests to specific columns in your models to ensure they behave as intended.

#### Singular Test
Singular tests or custom tests are specific to your project's requirements. These tests are written as SQL queries and are used to validate business logic or data quality that the generic tests cannot cover. For example, you might write a singular test to check if the total of all transaction amounts equals the reported total for a given period.

To run both types of tests on your models and seeds, use the following command:

```bash
dbt test
```

### Snapshot
Snapshots are a dbt feature that tracks changes to specific data in your data warehouse over time. They are particularly useful for capturing historical data that might otherwise be updated or deleted in the source system. Snapshots help preserve a version history of your data, which can be vital for audits, reporting, or analyzing trends.

To create a snapshot in dbt, you define snapshot models within your dbt project. These models specify the source data to track, the unique keys for identifying records, and the strategy for capturing changes (such as using a timestamp column or a log sequence number).

To execute snapshots and update your historical data tracking, use the following command:

```bash
dbt snapshot
```

### Generate and Serve dbt Docs
Generate and serve dbt documentation to visualize the data flow and model structures:

```bash
dbt docs generate
dbt docs serve --port 80
```

Access the documentation by visiting http://localhost:80.

## Models and Seeds

Here is a table of the dbt models and seeds used in this project:

| Type  | Schema          | Name                          | Description                                    |
|-------|-----------------|-------------------------------|------------------------------------------------|
| Model | modeling_data   | er_company_location           | Transformations on company locations           |
| Model | modeling_data   | er_degree                     | Degree details used in job listings            |
| Model | modeling_data   | er_job_type                   | Job types classifications                      |
| Model | modeling_data   | er_job                        | Main job details                               |
| Model | modeling_data   | er_major                      | Academic majors mentioned in listings          |
| Model | modeling_data   | er_tools                      | Tools mentioned in job listings                |
| Model | reporting_data  | rpt_data_role_by_edu          | Data roles categorized by educational level    |
| Model | reporting_data  | rpt_data_role_vacancy_trends  | Trends in job vacancies for data roles         |
| Model | reporting_data  | rpt_data_tools_by_data_role   | Tools used by different data roles             |
| Model | reporting_data  | rpt_data_tools_trends         | Trends in the usage of various tools           |
| Model | reporting_data  | rpt_job_fill_time_statistics  | Statistics on time taken to fill job vacancies |
| Model | reporting_data  | rpt_job_openings_geograph     | Geographic distribution of job openings        |
| Model | reporting_data  | rpt_job_openings_metrics      | Metrics related to job openings                |
| Model | reporting_data  | rpt_weekly_company_job_vacancies | Weekly vacancies reported by companies     |
| Seed  | modeling_data   | er_county                     | County data for location normalization         |
| Seed  | modeling_data   | er_district                   | District data for location normalization       |
| Seed  | modeling_data   | er_tools                      | Tools data for normalization                   |

## References
- [只會 SQL 也能成為資料工程師？用 DBT(data build tool) 解決資料團隊的缺糧危機](https://medium.com/dbt-local-taiwan/%E5%8F%AA%E6%9C%83sql%E4%B9%9F%E8%83%BD%E6%88%90%E7%82%BA%E8%B3%87%E6%96%99%E5%B7%A5%E7%A8%8B%E5%B8%AB-%E7%94%A8dbt-data-build-tool-%E8%A7%A3%E6%B1%BA%E8%B3%87%E6%96%99%E5%9C%98%E9%9A%8A%E7%9A%84%E7%BC%BA%E7%B3%A7%E5%8D%B1%E6%A9%9F-5e25c02dc41) - A medium article of basic dbt concept.

- [dbt Tutorial](https://ithelp.ithome.com.tw/users/20162689/ironman/6534) - A series of dbt tutorial on blog.

- [Code along - build an ELT Pipeline in 1 Hour (dbt, Snowflake, Airflow) - youtube](https://www.youtube.com/watch?v=OLXkGB7krGo) - A video tutorial on setting up an ELT pipeline using dbt and Snowflake.

- [Code along - build an ELT Pipeline in 1 Hour (dbt, Snowflake, Airflow) - notion](https://bittersweet-mall-f00.notion.site/Code-along-build-an-ELT-Pipeline-in-1-Hour-dbt-Snowflake-Airflow-cffab118a21b40b8acd3d595a4db7c15) - A notion to noted the script for an ELT pipeline using dbt and Snowflak.
