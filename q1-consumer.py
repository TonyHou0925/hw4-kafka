from confluent_kafka import Consumer
import json

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "youtube-comments"
KAFKA_CONFIG = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'youtube-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(KAFKA_CONFIG)
consumer.subscribe([KAFKA_TOPIC])

def main():
    video_likes = {}
    video_titles = {}
    
    print("Consumer is listening for messages...")
    
    while True:
        msg = consumer.poll(1.0)  # Poll for new messages
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        
        data = json.loads(msg.value().decode("utf-8"))
        video_id = data["video_id"]
        title = data["title"]
        likes = data["likes"]
        
        video_likes[video_id] = video_likes.get(video_id, 0) + likes
        video_titles[video_id] = title
        
        print(f"Received data: {data}")
        
        most_popular_video = max(video_likes, key=video_likes.get)
        print(f"Most popular video so far: {video_titles[most_popular_video]} with {video_likes[most_popular_video]} likes")

if __name__ == "__main__":
    main()