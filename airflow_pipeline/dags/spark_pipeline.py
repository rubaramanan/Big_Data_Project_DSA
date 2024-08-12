from datetime import datetime, timedelta

from airflow.decorators import dag, task
from scripts.hdfsHandler import Hdfs
from scripts.sparkHandler import Spark
from scripts.postgresqlHandler import save_data

default_args = {
    'owner': 'Ramanan',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


@dag(
    default_args=default_args,
    description='dag sending mock data to kafka',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 8, 1),
    catchup=False,
)
def etl():
    @task
    def extract():
        hdfs = Hdfs()
        return hdfs.read_csv('/user/hadoop/sales.csv')

    @task
    def transform(df):
        spark = Spark()
        return spark.transform(df)

    @task
    def load(df):
        save_data(df)

    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load(transformed_data)

dsa_dag = etl()
