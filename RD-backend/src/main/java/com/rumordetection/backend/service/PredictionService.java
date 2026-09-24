
package com.rumordetection.backend.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rumordetection.backend.entity.Prediction;
import com.rumordetection.backend.repository.PredictionRepository;

@Service
public class PredictionService {

    private final PredictionRepository predictionRepository;
    private final MlServiceClient mlServiceClient;
    private final ObjectMapper objectMapper;

    public PredictionService(
            PredictionRepository predictionRepository,
            MlServiceClient mlServiceClient,
            ObjectMapper objectMapper) {

        this.predictionRepository = predictionRepository;
        this.mlServiceClient = mlServiceClient;
        this.objectMapper = objectMapper;
    }

    // Create and save a new prediction
    public Prediction createPrediction(String text) {

        System.out.println("=================================");
        System.out.println("POST /api/predictions received");
        System.out.println("Text: " + text);
        System.out.println("Calling ML service...");

        // Call ML service
        MlPredictionResponse mlResponse =
                mlServiceClient.predict(text);

        System.out.println("ML service returned successfully");
        System.out.println("Result: " + mlResponse.getResult());
        System.out.println("Confidence: " + mlResponse.getConfidence());
        System.out.println("LIME explanation received");

        // Convert LIME explanation to JSON
        String limeExplanationJson;

        try {

            limeExplanationJson =
                    objectMapper.writeValueAsString(
                            mlResponse.getLime_explanation()
                    );

        } catch (JsonProcessingException e) {

            throw new IllegalStateException(
                    "Failed to convert LIME explanation to JSON",
                    e
            );
        }

        // Create Prediction entity
        Prediction prediction = new Prediction(
                text,
                mlResponse.getResult(),
                mlResponse.getConfidence(),
                limeExplanationJson
        );

        System.out.println("Saving prediction to MySQL...");

        // Save prediction to database
        Prediction savedPrediction =
                predictionRepository.save(prediction);

        System.out.println("Prediction saved successfully");
        System.out.println("ID: " + savedPrediction.getId());
        System.out.println(
                "LIME: " + savedPrediction.getLimeExplanation()
        );
        System.out.println("=================================");

        return savedPrediction;
    }

    // Get all predictions
    public List<Prediction> getAllPredictions() {

        return predictionRepository.findAll();
    }

    // Get prediction by ID
    public Prediction getPredictionById(Long id) {

        return predictionRepository
                .findById(id)
                .orElse(null);
    }
}


