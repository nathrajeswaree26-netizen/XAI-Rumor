package com.rumordetection.backend.service;

import java.util.List;

public class MlPredictionResponse {

    private String result;
    private double confidence;
    private double rumor_probability;
    private double non_rumor_probability;
    private List<LimeExplanation> lime_explanation;

    public MlPredictionResponse() {
    }

    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }

    public double getConfidence() {
        return confidence;
    }

    public void setConfidence(double confidence) {
        this.confidence = confidence;
    }

    public double getRumor_probability() {
        return rumor_probability;
    }

    public void setRumor_probability(double rumor_probability) {
        this.rumor_probability = rumor_probability;
    }

    public double getNon_rumor_probability() {
        return non_rumor_probability;
    }

    public void setNon_rumor_probability(double non_rumor_probability) {
        this.non_rumor_probability = non_rumor_probability;
    }

    public List<LimeExplanation> getLime_explanation() {
        return lime_explanation;
    }

    public void setLime_explanation(List<LimeExplanation> lime_explanation) {
        this.lime_explanation = lime_explanation;
    }

    public static class LimeExplanation {

        private String word;
        private double weight;

        public LimeExplanation() {
        }

        public String getWord() {
            return word;
        }

        public void setWord(String word) {
            this.word = word;
        }

        public double getWeight() {
            return weight;
        }

        public void setWeight(double weight) {
            this.weight = weight;
        }
    }
}