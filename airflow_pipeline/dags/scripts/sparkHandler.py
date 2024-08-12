import pandas as pd
from pyspark.sql import SparkSession


class Spark:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("Read CSV from HDFS to Spark") \
            .master("spark://192.168.2.79:7077") \
            .getOrCreate()

    def transform(self, df: pd.DataFrame):
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df.year = df.year.astype('i')
        df.month = df.month.astype('i')

        return self.spark.createDataFrame(df)
