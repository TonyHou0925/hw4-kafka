import json
from confluent_kafka import Consumer
from googleapiclient import discovery
import re

PROJECT_ID = "cloud-infrastructure-453220"
ZONE = "us-central1-a"
MACHINE_TYPE = f"zones/{ZONE}/machineTypes/e2-micro"
IMAGE_FAMILY = "debian-11"
IMAGE_PROJECT = "debian-cloud"

# Kafka Consumer Setup
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "queue-2"

consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'vm-creator-group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe([KAFKA_TOPIC])

def create_vm(author):
    compute = discovery.build('compute', 'v1')

    # Clean and validate VM name
    instance_name = re.sub(r'[^a-z0-9-]', '-', author.lower()).strip('-')
    if not instance_name[0].isalpha():
        instance_name = "vm-" + instance_name
    instance_name = instance_name[:61]  # Ensure max length 61

    # Define the boot disk
    disk = {
        "boot": True,
        "autoDelete": True,
        "initializeParams": {
            "sourceImage": f"projects/{IMAGE_PROJECT}/global/images/family/{IMAGE_FAMILY}"
        }
    }

    # Define the VM configuration
    config = {
        "name": instance_name,
        "machineType": MACHINE_TYPE,
        "disks": [disk],
        "networkInterfaces": [{
            "network": "global/networks/default",
            "accessConfigs": [{"type": "ONE_TO_ONE_NAT", "name": "External NAT"}]
        }]
    }

    try:
        operation = compute.instances().insert(
            project=PROJECT_ID,
            zone=ZONE,
            body=config
        ).execute()
        print(f"✅ VM '{instance_name}' creation started!")
    except Exception as e:
        print(f"❌ Error creating VM '{instance_name}': {e}")

def main():
    max_likes = -1
    top_author = None

    print("Listening for messages from Kafka...")

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            break  # Stop polling when no more messages

        data = json.loads(msg.value().decode("utf-8"))
        author = data["author"]
        likes = data["likes"]

        # ✅ Track the author with the most likes
        if likes > max_likes:
            max_likes = likes
            top_author = author

    if top_author:
        print(f"🏆 Most liked comment by '{top_author}' with {max_likes} likes!")
        create_vm(top_author)
    else:
        print("⚠️ No valid comments received.")

if __name__ == "__main__":
    main()
