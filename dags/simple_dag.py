import logging
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago


def _operation():
    logging.info("Hello world!")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}
dag = DAG(
    'hello_world',
    default_args=default_args,
    description='hello world',
    schedule_interval='@once',
    tags=["simple"]
)

start = DummyOperator(
    task_id='start',
    dag=dag
)

say_hello = PythonOperator(
    task_id='say_hello',
    python_callable=_operation,
    dag=dag
)

end = DummyOperator(
    task_id='end',
    dag=dag
)


start >> say_hello >> end
