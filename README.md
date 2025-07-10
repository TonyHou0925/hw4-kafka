# Homework 4: Apache Kafka – YouTube Comment Pipeline

This project was completed as part of **14-848 Cloud Infrastructure (Spring 2025)** at Carnegie Mellon University. It demonstrates a real-time data processing pipeline using **Apache Kafka**, the **YouTube Data API**, and **Google Cloud Platform (GCP)**. The project includes streaming message queues, DevOps-style pipeline design, and cloud automation.

## Project Summary

The homework consists of three main components:

### Q1: YouTube Comment Popularity via Kafka
- Accepts up to five YouTube video IDs as user input.
- A Kafka producer fetches comment data from the YouTube API.
- A consumer calculates total likes per video and identifies the most-liked one.
- Kafka topic used for communication between producer and consumer.

### Q2: Multi-Stage Kafka-Based Processing Pipeline
- Program 1: Retrieves YouTube comments and publishes to Kafka Queue-1.
- Programs 3 & 4: Load-balanced comment processing.
  - Each handles one video’s comments and filters those with positive like counts.
  - Publishes filtered results to Kafka Queue-2.
- Program 2: Aggregates results and displays video titles with like totals.
- Program 5: Creates a GCP VM named after the author of the most-liked comment.

### Q3: Kafka in Microservice Orchestration
- Updated Homework 3’s microservice orchestration app to insert Kafka between `WebApp` and `Logic` microservices.
- Deployed the full system on **Google Kubernetes Engine (GKE)**.
- Demonstrated successful message delivery and response via Kafka.

## Technologies Used

- Apache Kafka
- Python (Producer & Consumer)
- YouTube Data API v3
- Google Cloud Platform (VM & GKE)
- Kubernetes
- Docker

## Deliverables

- Source code for all Kafka programs and microservices
- Screenshots showing Kafka message topics and VM creation
- Output logs from Kafka consumers
- GKE deployment video demo

## Course Information

- Course: 14-848 Cloud Infrastructure
- Instructor: Mohamed Far