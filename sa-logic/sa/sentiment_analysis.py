from confluent_kafka import Consumer, KafkaException
import json

def consume_kafka():
    conf = {
        'bootstrap.servers': 'kafka-service:9092',
        'group.id': 'sentiment-group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)
    consumer.subscribe(['sentiment_requests'])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # Print raw Kafka message
        print(f"Raw Kafka Message: {msg.value()}")

        # Decode and parse the JSON message
        try:
            sentence = json.loads(msg.value().decode('utf-8'))
            print(f"Processed JSON: {sentence}")
        except Exception as e:
            print(f"Error decoding message: {e}")

if __name__ == "__main__":
    consume_kafka()
