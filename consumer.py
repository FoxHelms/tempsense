from kafka import KafkaConsumer
from prometheus_client import Gauge, start_http_server
import json
from influx_writer import InfluxWriter
from dotenv import load_dotenv

load_dotenv()

TOPICS = ["room.temp"]
BOOTSTRAP_SERVERS = ["localhost:9092"]
script_status = Gauge('consumer_script_running', 'consuer script up and running')

def handle_temp(data, influx):
    influx.write_temp(data)

TOPIC_HANDLERS = {"room.temp":handle_temp}

def start_consumer():
    consumer = KafkaConsumer(
        *TOPICS,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='latest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        key_deserializer=lambda k: k.decode('utf-8') if k else None
    )
    script_status.set(1)

    influx = InfluxWriter()

    try:
        for msg in consumer:
            topic = msg.topic
            print(f'Current topic:{topic}')
            data = msg.value
            handler = TOPIC_HANDLERS.get(topic)

            if handler:
                handler(data, influx)
                print(f"Received: {data}")
            else:
                print(f"No handler for topic: {topic}")
    except Exception as e:
        script_status.set(0)
        print(f'Error with consumer: {e}')


if __name__ == "__main__":
    start_http_server(8082)
    start_consumer()