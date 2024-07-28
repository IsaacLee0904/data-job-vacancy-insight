from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.telegram.operators.telegram import TelegramOperator
from datetime import datetime, timedelta
import pendulum

def notify_failure(context):
    execution_date  = pendulum_datetime.from_timestamp(context['execution_date'].timestamp(), tz='Asia/Taipei').strftime('%Y-%m-%d')
    failed_alert = TelegramOperator(
        task_id='send_failure_alert',
        telegram_conn_id='telegram_bot',
        chat_id='*********',
        text=f"🚨 Alert! Airflow weekly scheduled `job_vacancy_data_pipeline` has failed.\n\n🛠 Task: {context['task_instance_key_str']}\n\n📅 Execution Date: {execution_date}\n❌ Status: Failed\n\nPlease check the logs and resolve the issues.",
        dag=dag
    )
    return failed_alert.execute(context=context)

def notify_success(context):
    execution_date  = pendulum_datetime.from_timestamp(context['execution_date'].timestamp(), tz='Asia/Taipei').strftime('%Y-%m-%d')
    success_alert = TelegramOperator(
        task_id='send_success_alert',
        telegram_conn_id='telegram_bot',
        chat_id='*********',
        text=f"🎉 Congratulations! Airflow weekly scheduled `job_vacancy_data_pipeline` has successfully completed!\n\n🔍 Please review the results and ensure all data processing went smoothly.\n\n📅 Execution Date: {execution_date}\n\n✅ Status: Success",
        dag=dag
    )
    return success_alert.execute(context=context)

# DAG settings 
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 21, tzinfo=pendulum.timezone('Asia/Taipei')),
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
    task_id='transform_data_with_dbt',
    bash_command='docker exec -i data-job-vacancy-insight-app-1 bash -c "cd dbt && dbt run && dbt test && dbt snapshot"',
    dag=dag,
)

crawl_data >> load_raw_data >> transform_raw_data >> run_dbt
