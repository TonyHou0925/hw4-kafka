package com.sa.web;

import com.sa.web.dto.SentenceDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.web.bind.annotation.*;

@CrossOrigin(origins = "*")
@RestController
public class SentimentController {
    
    private static final String TOPIC = "sentiment_requests";

    @Autowired
    private KafkaTemplate<String, SentenceDto> kafkaTemplate;

    @PostMapping("/sentiment")
    public String sentimentAnalysis(@RequestBody SentenceDto sentenceDto) {
        System.out.println("Received from API: " + sentenceDto);
        kafkaTemplate.send(TOPIC, sentenceDto);
        System.out.println("Sent to Kafka: " + sentenceDto);
        return "Message sent to Kafka";
    }
    

    @GetMapping("/testHealth")
    public void testHealth() {
    }
}



