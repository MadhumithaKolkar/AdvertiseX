from kafka import KafkaConsumer
import json
import csv
import avro.schema
import avro.io
import io

# Kafka configuration
KAFKA_SERVER = 'localhost:9092'
KAFKA_TOPIC_IMPRESSIONS = 'ad_impressions'
KAFKA_TOPIC_CLICKS = 'ad_clicks'
KAFKA_TOPIC_BID_REQUESTS = 'bid_requests'

consumer_impressions = KafkaConsumer(
    KAFKA_TOPIC_IMPRESSIONS,
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset='earliest'
)

consumer_clicks = KafkaConsumer(
    KAFKA_TOPIC_CLICKS,
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset='earliest'
)

consumer_bid_requests = KafkaConsumer(
    KAFKA_TOPIC_BID_REQUESTS,
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset='earliest'
)

def process_impression(message):
    data = json.loads(message.value.decode('utf-8'))
    print(f"Processed impression: {data}")

def process_click(message):
    data = message.value.decode('utf-8').split(',')
    print(f"Processed click: {data}")

def process_bid_request(message):
    schema = avro.schema.Parse(open("bid_request.avsc", "r").read())
    bytes_reader = io.BytesIO(message.value)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    reader = avro.io.DatumReader(schema)
    bid_request = reader.read(decoder)
    print(f"Processed bid request: {bid_request}")

if __name__ == "__main__":
    for message in consumer_impressions:
        process_impression(message)
    for message in consumer_clicks:
        process_click(message)
    for message in consumer_bid_requests:
        process_bid_request(message)
