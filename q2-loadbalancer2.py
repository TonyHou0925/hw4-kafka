from confluent_kafka import Consumer, Producer
import json

KAFKA_BROKER = "localhost:9092"
INPUT_TOPIC = "queue-1"
OUTPUT_TOPIC = "queue-2"

consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'load-balancer-group',  # ✅ Shared group for auto-balancing
    'auto.offset.reset': 'earliest'
})
consumer.subscribe([INPUT_TOPIC])

producer = Producer({'bootstrap.servers': KAFKA_BROKER})

def main():
    print("✅ Load Balancer Program-4 started...")

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue

        data = json.loads(msg.value().decode("utf-8"))
        likes = data["likes"]

        print(f"Program-4 processing: {data}")

        # ✅ Publish only positive-like comments to queue-2
        if likes > 0:
            producer.produce(OUTPUT_TOPIC, value=json.dumps(data))
            print(f"Program-4 published: {data}")

        producer.flush()

if __name__ == "__main__":
    main()


