package com.rumordetection.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.rumordetection.backend.entity.Prediction;

public interface PredictionRepository extends JpaRepository<Prediction, Long> {
}