from googleapiclient.discovery import build
from confluent_kafka import Producer
import json

# YouTube API Setup
YOUTUBE_API_KEY = "AIzaSyA9ePimX4y5EW9ECKTHfIEPFmfIpZ4Okoc"
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Kafka Producer Setup
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "queue-1"
producer = Producer({'bootstrap.servers': KAFKA_BROKER})

def get_video_title(video_id):
    """Fetch the video title using the YouTube API."""
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    
    if response.get("items"):
        return response["items"][0]["snippet"]["title"]
    return "Unknown Title"

def get_comments(video_id):
    """Fetch comments, authors, and like counts from a YouTube video."""
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100
    )
    response = request.execute()

    comments = []
    for item in response.get("items", []):
        snippet = item["snippet"]["topLevelComment"]["snippet"]
        comments.append({
            "video_id": video_id,
            "video_title": get_video_title(video_id),
            "author": snippet["authorDisplayName"],
            "comment": snippet["textOriginal"],
            "likes": snippet["likeCount"]
        })
    return comments

def main():
    video_ids = input("Enter up to 5 YouTube video IDs (comma-separated): ").split(",")

    for video_id in video_ids:
        comments = get_comments(video_id.strip())
        for comment in comments:
            producer.produce(KAFKA_TOPIC, key=video_id.strip(), value=json.dumps(comment))
            print(f"Published: {comment}")

    producer.flush()

if __name__ == "__main__":
    main()
