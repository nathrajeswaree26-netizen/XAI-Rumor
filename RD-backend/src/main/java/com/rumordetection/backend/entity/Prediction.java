package com.rumordetection.backend.entity;

import java.time.LocalDateTime;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "predictions")
public class Prediction {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String text;

    @Column(nullable = false)
    private String result;

    @Column(nullable = false)
    private Double confidence;

    @Column(columnDefinition = "TEXT")
    private String limeExplanation;

    @Column(nullable = false)
    private LocalDateTime createdAt;

    public Prediction() {
    }

    public Prediction(
            String text,
            String result,
            Double confidence,
            String limeExplanation) {

        this.text = text;
        this.result = result;
        this.confidence = confidence;
        this.limeExplanation = limeExplanation;
        this.createdAt = LocalDateTime.now();
    }

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

    public String getLimeExplanation() {
        return limeExplanation;
    }

    public void setLimeExplanation(String limeExplanation) {
        this.limeExplanation = limeExplanation;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}