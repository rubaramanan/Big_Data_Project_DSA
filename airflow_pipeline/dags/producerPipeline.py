from datetime import datetime, timedelta

from airflow.decorators import dag, task

from scripts.kafkaHandler import Producer, Consumer

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


@dag(
    default_args=default_args,
    description='A simple tutorial DAG using the @dag and @task decorators',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 8, 1),
    catchup=False,
)
def kafka():
    @task
    def producer_pipeline():
        prod = Producer()
        prod.produce()
        prod.close()

    producer_pipeline()


kafka()
