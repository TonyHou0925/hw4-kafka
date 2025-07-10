FROM openjdk:17
WORKDIR /app

# Copy the built JAR file
COPY target/sentiment-analysis-web-0.0.1-SNAPSHOT.jar sentiment-analysis-web.jar

# Ensure application.properties is correctly packaged inside the JAR
CMD ["java", "-jar", "sentiment-analysis-web.jar"]

