from googleapiclient.discovery import build
from confluent_kafka import Producer
import json
import os

# Set up YouTube API key
YOUTUBE_API_KEY = #API KEY
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Confluent Kafka Configuration
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "youtube-comments"
KAFKA_CONFIG = {
    'bootstrap.servers': KAFKA_BROKER
}

producer = Producer(KAFKA_CONFIG)

def get_comment_likes(video_id):
    """Fetch total likes from comments of a YouTube video."""
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100  # Adjust as needed
    )
    response = request.execute()
    
    total_likes = 0
    for item in response.get("items", []):
        comment = item["snippet"]["topLevelComment"]["snippet"]
        total_likes += comment.get("likeCount", 0)
    
    return total_likes

def get_video_title(video_id):
    """Fetch video title."""
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    if response["items"]:
        return response["items"][0]["snippet"]["title"]
    return "Unknown Title"

def delivery_report(err, msg):
    """Delivery report for Kafka messages."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def main():
    video_ids = input("Enter up to 5 YouTube video IDs (comma-separated): ").split(",")
    
    for video_id in video_ids:
        video_id = video_id.strip()
        likes = get_comment_likes(video_id)
        title = get_video_title(video_id)
        data = {"video_id": video_id, "title": title, "likes": likes}
        
        producer.produce(KAFKA_TOPIC, key=video_id, value=json.dumps(data), callback=delivery_report)
        print(f"Sent: {data}")
    
    producer.flush()
    print("Data sent successfully!")

if __name__ == "__main__":
    main()
