from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.telegram.operators.telegram import TelegramOperator
from datetime import datetime, timedelta

def notify_failure(context):
    failed_alert = TelegramOperator(
        task_id='send_failure_alert',
        telegram_conn_id='telegram_bot',
        chat_id='*********', # need to replace with your chat_id
        text=f"Task {context['task_instance_key_str']} failed.",
        dag=dag
    )
    return failed_alert.execute(context=context)

def notify_success(context):
    success_alert = TelegramOperator(
        task_id='send_success_alert',
        telegram_conn_id='telegram_bot',
        chat_id='*********', # need to replace with your chat_id
        text="DAG job_vacancy_data_pipeline completed successfully!",
        dag=dag
    )
    return success_alert.execute(context=context)

# DAG settings 
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': notify_failure
}

dag = DAG(
    'job_vacancy_data_pipeline',
    default_args=default_args,
    description='A simple DAG to run data pipelines for job vacancy data processing',
    schedule_interval='0 0 * * 1',  # Set schedule interval to every Monday at midnight
    catchup=False,
    on_success_callback=notify_success
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
