from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

# DAG settings 
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email': ['hool19965401@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'job_vacancy_data_pipeline',
    default_args=default_args,
    description='A simple DAG to run data pipelines for job vacancy project testing',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

# task : load raw data in Docker 
buildup_test = DockerOperator(
    task_id='load_raw_data',
    image='data-job-vacancy-insight-app',
    api_version='auto',
    auto_remove=True,
    command='python src/buildup_src/package_checker.py',
    docker_url='unix://var/run/docker.sock',  # Docker Daemon socket
    network_mode='bridge',
    dag=dag,
)

# task：run dbt in Docker
run_dbt_test = DockerOperator(
    task_id='run_dbt',
    image='data-job-vacancy-insight-app',
    api_version='auto',
    auto_remove=True,
    command='bash -c "cd dbt && dbt run && dbt test && dbt snapshot"',
    docker_url='unix://var/run/docker.sock',  # Docker Daemon socket
    network_mode='bridge',
    dag=dag,
)

buildup_test >> run_dbt_test
