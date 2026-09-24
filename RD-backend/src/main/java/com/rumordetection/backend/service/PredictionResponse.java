package com.rumordetection.backend.service;

import java.time.LocalDateTime;
import java.util.List;

public class PredictionResponse {

    private Long id;
    private String text;
    private String result;
    private Double confidence;
    private List<LimeItem> limeExplanation;
    private LocalDateTime createdAt;

    // ============================================
    // Default Constructor
    // ============================================

    public PredictionResponse() {
    }

    // ============================================
    // Parameterized Constructor
    // ============================================

    public PredictionResponse(
            Long id,
            String text,
            String result,
            Double confidence,
            List<LimeItem> limeExplanation,
            LocalDateTime createdAt) {

        this.id = id;
        this.text = text;
        this.result = result;
        this.confidence = confidence;
        this.limeExplanation = limeExplanation;
        this.createdAt = createdAt;
    }

    // ============================================
    // Getters and Setters
    // ============================================

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }


    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }


    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }


    public Double getConfidence() {
        return confidence;
    }

    public void setConfidence(Double confidence) {
        this.confidence = confidence;
    }


    public List<LimeItem> getLimeExplanation() {
        return limeExplanation;
    }

    public void setLimeExplanation(
            List<LimeItem> limeExplanation) {

        this.limeExplanation = limeExplanation;
    }


    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(
            LocalDateTime createdAt) {

        this.createdAt = createdAt;
    }


    // ============================================
    // LIME ITEM
    // ============================================

    public static class LimeItem {

        private String word;
        private Double weight;

        // ----------------------------------------
        // Default Constructor
        // ----------------------------------------

        public LimeItem() {
        }

        // ----------------------------------------
        // Parameterized Constructor
        // ----------------------------------------

        public LimeItem(
                String word,
                Double weight) {

            this.word = word;
            this.weight = weight;
        }

        // ----------------------------------------
        // Get Word
        // ----------------------------------------

        public String getWord() {
            return word;
        }

        // ----------------------------------------
        // Set Word
        // ----------------------------------------

        public void setWord(String word) {
            this.word = word;
        }

        // ----------------------------------------
        // Get Weight
        // ----------------------------------------

        public Double getWeight() {
            return weight;
        }

        // ----------------------------------------
        // Set Weight
        // ----------------------------------------

        public void setWeight(Double weight) {
            this.weight = weight;
        }
    }
}