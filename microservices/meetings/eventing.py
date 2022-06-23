from json import loads
from kafka import KafkaConsumer
from dotenv import load_dotenv
import os

import database

load_dotenv()

class Consumer:
    consumer: KafkaConsumer

    def __init__(self, topic: str):
        environment = os.getenv("ENVIRONMENT")
        
        dev_agrs = {
            "bootstrap_servers": "meetup-clone_kafka_1:9092",
        }

        prod_args = {
            "bootstrap_servers":os.getenv("AIVEN_BOOTSTRAP_SERVER"),
            "security_protocol":"SASL_SSL",
            "sasl_mechanism":"PLAIN",
            "sasl_plain_username":os.getenv("AIVEN_SASL_USERNAME"),
            "sasl_plain_password":os.getenv("AIVEN_SASL_PASSWORD"),
            # ssl_cafile="ca.pem"
        }

        args = prod_args if environment == "prod" else dev_agrs
        
        self.consumer = KafkaConsumer(
            topic,
            group_id="meetings-consumer",
            auto_offset_reset="earliest",
            value_deserializer=lambda x: loads(x.decode('utf-8')),
            **args
        )
    
    def pool(self):
        return self.consumer
    
def listen_events():
    pool = Consumer("category.renamed").pool()
    print("start listen")
    for msg in pool:
        print(msg.value)
        update_meetings_category_name(
            category_id=msg.value["category_id"],
            category_name=msg.value["name"]
        )
        

def update_meetings_category_name(category_id: str, category_name: str):
    conn = database.create_server_connection()
    cursor = conn.cursor()

    query_update = """UPDATE meetings SET category_name = %s WHERE category_id = %s"""
    cursor.execute(query_update, (category_name, category_id))
    
    conn.commit()