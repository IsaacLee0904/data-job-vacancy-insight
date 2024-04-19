# Data-Job-Vacancy-Insight
A system that recommends data-centric jobs and provides insights, featuring a personalized job report service delivered through a Telegram bot.

## Authors 
- [@IsaacLee0904](https://github.com/IsaacLee0904)

## Timeline
- **2024-03-25:** Project workflow design
- **2024-03-26:** Set up development environment with Docker
- **2024-03-28 to 2024-03-31:** Development of 104 crawler
- **2024-03-31:** Database design
- **2024-04-01 to 2024-04-02:** Data pipeline - Load raw data into the data warehouse (source_data layer)
- **2024-04-08 to 2024-04-09:** Data pipeline - Transform data in the data warehouse (staging_data layer)
- **2024-04-09 to 2024-04-10:** Set up DBT (Data Build Tool)
- **2024-04-12 to 2024-04-19:** Data pipeline - Transform data into the data warehouse (modeling_data layer) with dbt
    - ER model build up in modeling_data layer with dbt model feature
    - ER model tables data quality check setup with dbt test feature
    - Data warehouse modeling_data layer graph (http://localhost:80)
    - Data warehouse modeling_data layer change data capture(CDC) setup with dbt snapshot feature (non-finished)
- Data pipeline deploy with airflow (to-do)
    - 104 crawler
    - Data pipeline - load raw data
    - Data pipeline - transform data
    - Data pipeline - ER modeling 
    - Data quality check 
    - Change data capture

## Project Overview
The "Data-Job-Vacancy-Insight" project is designed to streamline the job searching process for data professionals. By aggregating and analyzing job listings from multiple sources, it offers personalized job recommendations and valuable market insights directly through a user-friendly Telegram bot interface.

## Features
- **Job Recommendations:** Tailored suggestions based on user's skills and preferences.
- **Market Insights:** Analysis of current job market trends within the data field.
- **User Profiles:** Customizable profiles that enhance job matching accuracy.
- **Automated Reports:** Regular updates and reports delivered through Telegram.