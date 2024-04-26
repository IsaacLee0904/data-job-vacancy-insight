from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

# DAG settings 
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 29),  # Set start date to April 29, 2024
    'email': ['hool19965401@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
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

# task : load raw data in Docker 
load_raw_data = DockerOperator(
    task_id='load_raw_data',
    image='data-job-vacancy-insight-app',
    api_version='auto',
    auto_remove=False,
    command='python src/data_processing_src/load_raw_data.py',
    docker_url='unix://var/run/docker.sock',  # Docker Daemon socket
    network_mode='bridge',
    dag=dag,
)

# task：transform raw data in Docker
transform_raw_data = DockerOperator(
    task_id='transform_raw_data',
    image='data-job-vacancy-insight-app',
    api_version='auto',
    auto_remove=False,
    command='python src/data_processing_src/transform_raw_data.py',
    docker_url='unix://var/run/docker.sock',  # Docker Daemon socket
    network_mode='bridge',
    dag=dag,
)

# task：run dbt in Docker
run_dbt = DockerOperator(
    task_id='run_dbt',
    image='data-job-vacancy-insight-app',
    api_version='auto',
    auto_remove=False,
    command='bash -c "cd dbt && dbt run && dbt test && dbt snapshot"',
    docker_url='unix://var/run/docker.sock',  # Docker Daemon socket
    network_mode='bridge',
    dag=dag,
)

load_raw_data >> transform_raw_data >> run_dbt
