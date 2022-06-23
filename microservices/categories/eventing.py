from dataclasses import dataclass
from kafka import KafkaProducer, Serializer
import json
from dotenv import load_dotenv
import os

load_dotenv()

class Producer:
    producer: KafkaProducer
    user: str

    def __init__(self) -> None:
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
        self.producer = KafkaProducer(
            client_id="categories-producer",
            acks=1,
            retries=3,
            max_in_flight_requests_per_connection=1,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            **args
            # prod
            
        )
    
    def publish_message(
        self,
        topic: str,
        message: dict,
    ) -> None: 
        self.producer.send(
            topic,
            message,
            # key=b"some.key",
        ).add_callback(self._on_send_success).add_errback(self._on_send_error)

        self.producer.flush()

    def _on_send_success(self, record_metadata):
        print(record_metadata)
        print(f"{record_metadata.topic}/partition={record_metadata.partition}/offset={record_metadata.offset}")

    def _on_send_error(self, exception):
        print(exception)

@dataclass
class CategoryEvents:
    producer: Producer

    def category_renamed(self, id: int, name: str):
        self.producer.publish_message(
            topic="category.renamed",
            message={
                "category_id": id,
                "name": name
            }
        )

    