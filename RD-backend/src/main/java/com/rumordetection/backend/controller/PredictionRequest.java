package com.rumordetection.backend.controller;

import jakarta.validation.constraints.NotBlank;

public class PredictionRequest {

    @NotBlank(message = "Text cannot be empty")
    private String text;

    public PredictionRequest() {
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }
}