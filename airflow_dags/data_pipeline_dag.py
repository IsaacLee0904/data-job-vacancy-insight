from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# DAG settings 
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),  # Set start date to April 22, 2024
    'email': ['hool19965401@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'job_vacancy_data_pipeline',
    default_args=default_args,
    description='A simple DAG to run data pipelines for job vacancy data processing',
    schedule_interval='0 0 * * 1',  # Set schedule interval to every Monday at midnight
    catchup=False,
)

# task : crawl data from 104 
crawl_data = BashOperator(
    task_id='crawl_data_from_104',
    bash_command='docker exec -i data-job-vacancy-insight-app-1 python /app/src/crawler_src/104_crawler.py',
    dag=dag,
)

# task : load raw data in Docker 
load_raw_data = BashOperator(
    task_id='load_raw_data',
    bash_command='docker exec -i data-job-vacancy-insight-app-1 python /app/src/data_processing_src/load_raw_data.py',
    dag=dag,
)

# task：transform raw data in Docker
transform_raw_data = BashOperator(
    task_id='transform_raw_data',
    bash_command='docker exec -i data-job-vacancy-insight-app-1 python /app/src/data_processing_src/transform_raw_data.py',
    dag=dag,
)

# task：run dbt in Docker
run_dbt = BashOperator(
    task_id='build_er_model_with_dbt',
    bash_command='docker exec -i data-job-vacancy-insight-app-1 bash -c "cd dbt && dbt run && dbt test && dbt snapshot"',
    dag=dag,
)

crawl_data >> load_raw_data >> transform_raw_data >> run_dbt
