
package com.rumordetection.backend.service;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import com.fasterxml.jackson.databind.ObjectMapper;

@Component
public class MlServiceClient {

    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    private final String mlServiceUrl;

    public MlServiceClient(
            @Value("${ml.service.url:http://127.0.0.1:8001}") String mlServiceUrl) {

        this.httpClient = HttpClient.newBuilder()
                .version(HttpClient.Version.HTTP_1_1)
                .build();

        this.objectMapper = new ObjectMapper();

        this.mlServiceUrl = mlServiceUrl;
    }

    public MlPredictionResponse predict(String text) {

        try {

            String jsonBody =
                    objectMapper.writeValueAsString(
                            new MlPredictionRequest(text)
                    );

            String predictUrl =
                    mlServiceUrl + "/predict";

            System.out.println("=================================");
            System.out.println("Sending request to ML service");
            System.out.println("ML URL: " + predictUrl);
            System.out.println("JSON Body: " + jsonBody);
            System.out.println("Body Length: " + jsonBody.length());
            System.out.println("=================================");

            HttpRequest httpRequest =
                    HttpRequest.newBuilder()
                            .uri(URI.create(predictUrl))
                            .version(HttpClient.Version.HTTP_1_1)
                            .header(
                                    "Content-Type",
                                    "application/json"
                            )
                            .header(
                                    "Accept",
                                    "application/json"
                            )
                            .POST(
                                    HttpRequest.BodyPublishers
                                            .ofString(jsonBody)
                            )
                            .build();

            System.out.println(
                    "HTTP request created successfully"
            );

            System.out.println(
                    "Sending request..."
            );

            HttpResponse<String> response =
                    httpClient.send(
                            httpRequest,
                            HttpResponse.BodyHandlers.ofString()
                    );

            System.out.println(
                    "ML Service HTTP Status: "
                            + response.statusCode()
            );

            System.out.println(
                    "ML Service Response: "
                            + response.body()
            );

            if (response.statusCode() < 200
                    || response.statusCode() >= 300) {

                throw new RuntimeException(
                        "ML service returned HTTP "
                                + response.statusCode()
                                + ": "
                                + response.body()
                );
            }

            return objectMapper.readValue(
                    response.body(),
                    MlPredictionResponse.class
            );

        } catch (IOException e) {

            throw new RuntimeException(
                    "Failed to communicate with ML service at "
                            + mlServiceUrl
                            + "/predict",
                    e
            );

        } catch (InterruptedException e) {

            Thread.currentThread().interrupt();

            throw new RuntimeException(
                    "ML service request was interrupted",
                    e
            );
        }
    }
}

