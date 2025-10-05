import os, sys, time
from dotenv import load_dotenv
from datetime import datetime
from kafka import KafkaProducer
import requests
import json

load_dotenv()

weather_url = os.getenv('WEATHER_URL', 'No weather url found')
cachedResponse = {"humidity":5, "temp_f":70.00}

def fetch_data_from_http(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        cachedResponse = response.json()
        return response.json()  # Assuming the endpoint returns JSON
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return cachedResponse


TOPIC = "room.temp"

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8')
)

while True:
    time.sleep(2)
    data = fetch_data_from_http(weather_url) # "{ 'humidity' : 5.00, 'temp_f': 72.00}"
#    time.sleep(1)
    print(data)
    try:
        tempDict = data
    except:
        tempDict = cached_dict
    temp_json = {
        "humidity": tempDict["humidity"],
        "temp_f": tempDict["temp_f"],
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": "room_temperature_sensor"
    }

    producer.send(
        TOPIC,
        key=temp_json["source"],
        value=temp_json
    )
    cached_dict = tempDict
    print(f"Sent: {temp_json}")
