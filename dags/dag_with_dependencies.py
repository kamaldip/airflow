import logging
from datetime import timedelta

# Testing we can import PIP modules using the `requirements.txt` file
import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

# Testing we can import a value from a package within the DAGs folder in S3
from dependencies.config import sample_config_value


def _operation():
    logging.info(sample_config_value)
    df = pd.DataFrame(data={
        "A": [1, 2],
        "B": [3, 4]
    })
    logging.info(df["A"])


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

check_dependencies = PythonOperator(
    task_id='check_dependencies',
    python_callable=_operation,
    dag=dag
)

end = DummyOperator(
    task_id='end',
    dag=dag
)


start >> check_dependencies >> end
