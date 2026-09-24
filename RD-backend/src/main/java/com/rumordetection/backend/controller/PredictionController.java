package com.rumordetection.backend.controller;

import java.util.ArrayList;
import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rumordetection.backend.entity.Prediction;
import com.rumordetection.backend.service.PredictionResponse;
import com.rumordetection.backend.service.PredictionService;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/predictions")
@CrossOrigin(
        origins = {
                "http://localhost:5173",
                "http://localhost:5174",
                "http://127.0.0.1:5173",
                "http://127.0.0.1:5174"
        }
)
public class PredictionController {

    private final PredictionService predictionService;
    private final ObjectMapper objectMapper;

    public PredictionController(
            PredictionService predictionService) {

        this.predictionService = predictionService;
        this.objectMapper = new ObjectMapper();
    }

    // ==========================================
    // CREATE NEW PREDICTION
    // POST /api/predictions
    // ==========================================

    @PostMapping
    public ResponseEntity<PredictionResponse> createPrediction(
            @Valid @RequestBody PredictionRequest request) {

        Prediction prediction =
                predictionService.createPrediction(
                        request.getText()
                );

        return ResponseEntity.ok(
                convertToResponse(prediction)
        );
    }

    // ==========================================
    // GET ALL PREDICTIONS
    // GET /api/predictions
    // ==========================================

    @GetMapping
    public ResponseEntity<List<PredictionResponse>> getAllPredictions() {

        List<PredictionResponse> responses = new ArrayList<>();

        for (Prediction prediction :
                predictionService.getAllPredictions()) {

            responses.add(convertToResponse(prediction));
        }

        return ResponseEntity.ok(responses);
    }

    // ==========================================
    // GET PREDICTION BY ID
    // GET /api/predictions/{id}
    // ==========================================

    @GetMapping("/{id}")
    public ResponseEntity<PredictionResponse> getPredictionById(
            @PathVariable Long id) {

        Prediction prediction =
                predictionService.getPredictionById(id);

        if (prediction == null) {

            return ResponseEntity
                    .notFound()
                    .build();
        }

        return ResponseEntity.ok(
                convertToResponse(prediction)
        );
    }

    // ==========================================
    // CONVERT ENTITY TO RESPONSE
    // ==========================================

    private PredictionResponse convertToResponse(
            Prediction prediction) {

        List<PredictionResponse.LimeItem> limeItems =
                new ArrayList<>();

        try {

            if (prediction.getLimeExplanation() != null
                    && !prediction.getLimeExplanation().isBlank()
                    && !prediction.getLimeExplanation().equals("[]")) {

                limeItems = objectMapper.readValue(
                        prediction.getLimeExplanation(),
                        new TypeReference<List<PredictionResponse.LimeItem>>() {}
                );
            }

        } catch (Exception e) {

            System.out.println(
                    "Error parsing LIME explanation: "
                            + e.getMessage()
            );
        }

        return new PredictionResponse(
                prediction.getId(),
                prediction.getText(),
                prediction.getResult(),
                prediction.getConfidence(),
                limeItems,
                prediction.getCreatedAt()
        );
    }
}