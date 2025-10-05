from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from dotenv import load_dotenv

load_dotenv()

class InfluxWriter:
    def __init__(self, bucket="temp_data"):
        self.client = InfluxDBClient(
            url="http://localhost:8086",
            token="admin-token",
            org="market_data"
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.bucket = bucket

    def write_temp(self, data):
        point = (
            Point("temp_humidity")
            .tag("source", data["source"])
            .field("humidity", float(data["humidity"]))
            # .field("temp_c", float(data["temp_c"])) uncomment when reading from serial
            .field("temp_f", float(data["temp_f"]))
            .time(data["timestamp"])
        )
        self.write_api.write(bucket=self.bucket, record=point)
