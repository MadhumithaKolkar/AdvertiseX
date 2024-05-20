from kafka import KafkaProducer
import json
import csv
import avro.schema
import avro.io
import io
import random
import time

# Kafka configuration
KAFKA_TOPIC_IMPRESSIONS = 'ad_impressions'
KAFKA_TOPIC_CLICKS = 'ad_clicks'
KAFKA_TOPIC_BID_REQUESTS = 'bid_requests'
KAFKA_SERVER = 'localhost:9092'

# Kafka producer
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)


# Simulate sending ad impressions (JSON)
def send_ad_impressions():
    ad_impression = {
        'ad_creative_id': random.randint(1, 1000),
        'user_id': random.randint(1, 1000),
        'timestamp': int(time.time()),
        'website': 'example.com'
    }
    producer.send(KAFKA_TOPIC_IMPRESSIONS, json.dumps(ad_impression).encode('utf-8'))


# Simulate sending ad clicks and conversions (CSV)
def send_ad_clicks():
    ad_click = {
        'timestamp': int(time.time()),
        'user_id': random.randint(1, 1000),
        'ad_campaign_id': random.randint(1, 100),
        'conversion_type': 'purchase'
    }
    csv_data = ','.join(map(str, ad_click.values()))
    producer.send(KAFKA_TOPIC_CLICKS, csv_data.encode('utf-8'))


# Simulate sending bid requests (Avro)
def send_bid_requests():
    schema = avro.schema.Parse(open("bid_request.avsc", "r").read())
    writer = avro.io.DatumWriter(schema)
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)

    bid_request = {
        'user_id': random.randint(1, 1000),
        'auction_details': 'details',
        'ad_targeting_criteria': 'criteria'
    }
    writer.write(bid_request, encoder)
    raw_bytes = bytes_writer.getvalue()
    producer.send(KAFKA_TOPIC_BID_REQUESTS, raw_bytes)


if __name__ == "__main__":
    while True:
        send_ad_impressions()
        send_ad_clicks()
        send_bid_requests()
        time.sleep(1)
