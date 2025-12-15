from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from src.core.config import INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET

client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()
bucket = INFLUXDB_BUCKET
org = INFLUXDB_ORG
