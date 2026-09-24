# XAI-Rumor

## AI-Powered Explainable Rumor Detection System

XAI-Rumor is an AI-powered web-based Rumor Detection System designed to identify whether a given social media text is likely to be a **Rumor** or **Non-Rumor**. The system combines Natural Language Processing (NLP), Deep Learning, Machine Learning, and Explainable AI (XAI) to provide both a prediction and an understandable explanation of the model's decision.

The system uses **BERT (Bidirectional Encoder Representations from Transformers)** to generate contextual text embeddings and a **Random Forest classifier** to classify the extracted features. To improve transparency, **LIME (Local Interpretable Model-Agnostic Explanations)** is used to identify important words/features that contribute to an individual prediction.

The project follows a complete full-stack architecture consisting of a **React frontend, Spring Boot backend, FastAPI machine-learning service, and MySQL database**.

---

## 🎯 Project Objective

The main objective of XAI-Rumor is to develop an automated and explainable system for detecting potentially misleading information shared through social media.

Traditional machine-learning systems may provide only a final prediction without explaining why the prediction was generated. XAI-Rumor addresses this by combining rumor classification with explainability.

The system aims to:

- Detect whether social media text is **Rumor** or **Non-Rumor**
- Use BERT to capture contextual information from text
- Use Random Forest for classification
- Provide prediction confidence and class probabilities
- Use LIME to explain individual predictions
- Store prediction history in MySQL
- Provide an easy-to-use web interface
- Demonstrate an end-to-end AI and full-stack application

---

## ✨ Key Features

### 📰 Rumor Detection
The system analyzes user-provided text and classifies it as:

- **Rumor**
- **Non-Rumor**

### 🤖 BERT-Based Text Representation
BERT is used to transform input text into contextual numerical embeddings. These embeddings capture relationships and contextual information between words.

### 🌲 Random Forest Classification
The generated BERT embeddings are provided to a Random Forest classifier for the final classification.

### 🔍 Explainable AI with LIME
LIME provides an explanation for individual predictions by identifying words/features that contribute to the model's output.

### 📊 Prediction Confidence
The application displays the model's confidence and class probabilities along with the prediction.

### 💾 Prediction History
Prediction information can be stored in a MySQL database, allowing users to maintain and view previous predictions.

### 🌐 Full-Stack Web Application
The system integrates:

- React frontend
- Spring Boot backend
- FastAPI ML service
- MySQL database

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │    React Frontend    │
                         │      (Vite)          │
                         └──────────┬───────────┘
                                    │
                                    │ REST API
                                    ▼
                         ┌──────────────────────┐
                         │   Spring Boot API    │
                         │      Backend         │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP Request
                                    ▼
                         ┌──────────────────────┐
                         │   FastAPI ML Service │
                         │       Python         │
                         └──────────┬───────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
             ┌───────────────┐             ┌───────────────┐
             │      BERT     │             │ Random Forest │
             │  Embeddings   │────────────▶│  Classifier   │
             └───────────────┘             └───────┬───────┘
                                                   │
                                                   ▼
                                            ┌──────────────┐
                                            │     LIME     │
                                            │ Explanation  │
                                            └──────────────┘

                         Spring Boot Backend
                                  │
                                  ▼
                         ┌────────────────┐
                         │     MySQL      │
                         │    Database    │
                         └────────────────┘
