import serial, sys, time
from dotenv import load_dotenv
from datetime import datetime
from kafka import KafkaProducer
import json

port = "/dev/ttyUSB0"
baudrate = 9600
ser = serial.Serial(port,baudrate,timeout=0.001)
TOPIC = "room.temp"

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8')
)

while True:
    time.sleep(2)
    data = ser.readline()
#    data = ser.read(ser.inWaiting())
    data_string = data.decode() # "{ 'humidity' : 5.00, 'temp_c': 21.00, 'temp_f': 72.00}"
#    time.sleep(1)
    try:
        tempDict = json.loads(data_string)
    except:
        tempDict = cached_dict
    temp_json = {
        "humidity": tempDict["humidity"],
        "temp_c": tempDict["temp_c"],
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
