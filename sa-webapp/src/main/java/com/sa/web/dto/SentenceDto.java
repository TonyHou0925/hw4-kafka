package com.sa.web.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class SentenceDto {
    @JsonProperty("text") // Ensure "text" field is mapped correctly
    private String text;

    // Default constructor required for JSON deserialization
    public SentenceDto() {}

    public SentenceDto(String text) {
        this.text = text;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    @Override
    public String toString() {
        return "SentenceDto{text='" + text + "'}";
    }
}
