from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.telegram.operators.telegram import TelegramOperator
from datetime import datetime, timedelta
import pendulum

def notify_failure(context):
    execution_date  = pendulum_datetime.from_timestamp(context['execution_date'].timestamp(), tz='Asia/Taipei').strftime('%Y-%m-%d')
    execution_date  = context['execution_date'].strftime('%Y-%m-%d %H:%M:%S')
    failed_alert = TelegramOperator(
        task_id='send_failure_alert',
        telegram_conn_id='telegram_bot',
        chat_id='*********', # need to replace with your chat_id
        text=f"🚨 Alert! Airflow weekly scheduled `job_vacancy_data_pipeline` has failed.\n\n🛠 Task: {context['task_instance_key_str']}\n📅 Execution Date: {context['execution_date']}\n❌ Status: Failed\n\nPlease check the logs and resolve the issues.",
        dag=dag
    )
    return failed_alert.execute(context=context)

def notify_success(context):
    success_alert = TelegramOperator(
        task_id='send_success_alert',
        telegram_conn_id='telegram_bot',
        chat_id='*********', # need to replace with your chat_id
        text="🎉 Congratulations! Airflow weekly scheduled `job_vacancy_data_pipeline` has successfully completed!\n\n🔍 Please review the results and ensure all data processing went smoothly.\n📅 Execution Date: {{ execution_date }}\n✅ Status: Success",
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
    'job_vacancy_deploy_sync',
    default_args=default_args,
    description='A simple DAG to sync deploy env for job vacancy dashboard',
    schedule_interval='0 1 * * 1',  # Set schedule interval to every Monday at midnight
    catchup=False,
    on_success_callback=notify_success
)

# task : sync deploy env data
sync_deploy_data = BashOperator(
    task_id='sync_deploy_data',
    bash_command='docker exec -i data-job-vacancy-insight-app-1 python /app/src/data_processing_src/sync_data_to_render.py',
    dag=dag,
)

sync_deploy_data 
