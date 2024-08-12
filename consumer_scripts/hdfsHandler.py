import pandas as pd
from hdfs import InsecureClient


class Hdfs:
    def __init__(self):
        self.hdfs_client = InsecureClient('http://172.17.0.1:9870',
                                          user='hadoop')

    def read(self, file: str):
        with self.hdfs_client.read(file, encoding='utf-8') as f:
            data = f.read()
            print(data)

    def read_csv(self, file: str):
        with self.hdfs_client.read(file) as reader:
            pandas_df = pd.read_csv(reader)

        return pandas_df

    def write(self, data: str, file: str):
        with self.hdfs_client.write(file, overwrite=True, encoding='utf-8') as writer:
            writer.write(data)
