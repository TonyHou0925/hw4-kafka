from confluent_kafka import Consumer
import json

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "queue-1"

consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'aggregator-group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe([KAFKA_TOPIC])

video_likes = {}  # ✅ Track likes per video separately

def main():
    print("Listening for messages from Kafka...")

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue

        data = json.loads(msg.value().decode("utf-8"))
        
        video_id = data["video_id"]
        title = data["video_title"]
        likes = data["likes"]

        # ✅ Aggregate likes per video
        if video_id in video_likes:
            video_likes[video_id]["likes"] += likes
        else:
            video_likes[video_id] = {"title": title, "likes": likes}

        # ✅ Print aggregated likes PER VIDEO (not total)
        print("\n🔹 Aggregated Likes Per Video:")
        for vid, info in video_likes.items():
            print(f"🎥 {info['title']}: {info['likes']} likes")

if __name__ == "__main__":
    main()

