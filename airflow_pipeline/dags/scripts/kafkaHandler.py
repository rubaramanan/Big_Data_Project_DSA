import datetime as dt
import json
import time

from kafka import KafkaProducer, KafkaConsumer

from scripts.hdfsHandler import Hdfs
from scripts.utils import json_serializer, json_deserializer, generate_sales_data


class Producer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['192.168.2.79:9092'],
            value_serializer=json_serializer,
            # acks='all',  # Ensure all replicas acknowledge
            # retries=1,  # Number of retries on failure
            # request_timeout_ms=30000,  # Request timeout
            # metadata_max_age_ms=60000  # Metadata refresh interval
        )

        print(f'Initialized Kafka producer at {dt.datetime.utcnow()}')

    def produce(self):
        sales_data = generate_sales_data()
        self.producer.send('transactions',
                           value=sales_data)
        time.sleep(0.5)

    def close(self):
        self.producer.flush()
        self.producer.close()


class Consumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'transactions',
            bootstrap_servers=['192.168.2.79:9092'],
            auto_offset_reset='earliest',  # Start reading at the earliest available message
            enable_auto_commit=True,  # Automatically commit offsets
            group_id='test_group',
            value_deserializer=json_deserializer,
            request_timeout_ms=30000,  # Request timeout
            session_timeout_ms=10000,  # Session timeout for consumer group
            max_poll_interval_ms=300000,  # Max interval between polls
            metadata_max_age_ms=60000  # Metadata refresh interval
        )

        print(f'Initialized Kafka consumer at {dt.datetime.utcnow()}')

    # def transform(self, message):
    #     mframe = pd.DataFrame(message)
    #
    #     mframe['date'] = pd.to_datetime(mframe['date'])
    #     mframe['year'] = mframe['date'].dt.year
    #     mframe['month'] = mframe['date'].dt.month
    #     mframe.year = mframe.year.astype('i')
    #     mframe.month = mframe.month.astype('i')
    #
    #     return mframe.to_dict('records')

    def load(self, parameters):
        print(parameters)
        if isinstance(parameters, (dict, list)):
            parameters = json.dumps(parameters)

        hdfs = Hdfs()
        hdfs.write(parameters, 'sales.csv')

    def consume(self):
        for message in self.consumer:
            # params = self.transform(message.value)
            # print(message)
            self.load(message.value)

    def close(self):
        self.consumer.close()
