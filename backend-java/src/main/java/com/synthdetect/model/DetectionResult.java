package com.synthdetect.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class DetectionResult {
    
    private String prediction;
    private Double confidence;
    
    @JsonProperty("fake_probability")
    private Double fakeProbability;
    
    @JsonProperty("real_probability")
    private Double realProbability;
    
    @JsonProperty("processing_time")
    private Double processingTime;

    // Default constructor
    public DetectionResult() {}
    
    // Constructor with basic fields
    public DetectionResult(String prediction, Double confidence) {
        this.prediction = prediction;
        this.confidence = confidence;
    }

    // Getters and Setters
    public String getPrediction() {
        return prediction;
    }

    public void setPrediction(String prediction) {
        this.prediction = prediction;
    }

    public Double getConfidence() {
        return confidence;
    }

    public void setConfidence(Double confidence) {
        this.confidence = confidence;
    }

    public Double getFakeProbability() {
        return fakeProbability;
    }

    public void setFakeProbability(Double fakeProbability) {
        this.fakeProbability = fakeProbability;
    }

    public Double getRealProbability() {
        return realProbability;
    }

    public void setRealProbability(Double realProbability) {
        this.realProbability = realProbability;
    }

    public Double getProcessingTime() {
        return processingTime;
    }

    public void setProcessingTime(Double processingTime) {
        this.processingTime = processingTime;
    }

    @Override
    public String toString() {
        return "DetectionResult{" +
                "prediction='" + prediction + '\'' +
                ", confidence=" + confidence +
                ", fakeProbability=" + fakeProbability +
                ", realProbability=" + realProbability +
                ", processingTime=" + processingTime +
                '}';
    }
}
