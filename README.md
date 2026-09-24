# 🔍 XAI-Rumor

### Explainable AI-Powered Rumor Detection System

XAI-Rumor is an AI-powered, full-stack web application designed to detect whether social media content is likely to be **Rumor** or **Non-Rumor** while providing an interpretable explanation of the prediction.

The system combines **Natural Language Processing (NLP), BERT, Machine Learning, Explainable AI (XAI), REST APIs, and full-stack web development** into a single application.

Unlike a traditional classification system that only displays a prediction, XAI-Rumor uses **LIME (Local Interpretable Model-Agnostic Explanations)** to provide important words/features that contributed to an individual prediction.

The application is developed using **React, Spring Boot, FastAPI, Python, BERT, Random Forest, LIME, and MySQL**.

---

## 🎯 Project Objective

The objective of XAI-Rumor is to develop an automated and explainable system for analyzing potentially misleading information shared through social media.

The system focuses on two important aspects:

1. **Rumor Detection** – classify the given text as Rumor or Non-Rumor.
2. **Explainability** – provide an understandable explanation for the individual prediction.

The project demonstrates how AI models can be integrated with a complete web application to create an interactive and explainable machine-learning solution.

---

## ✨ Key Features

* 📰 **Rumor / Non-Rumor Classification**
* 🤖 **BERT-based contextual text representation**
* 🌲 **Random Forest classification**
* 🔍 **LIME-based Explainable AI**
* 📊 **Prediction confidence**
* 📈 **Rumor and Non-Rumor probabilities**
* 💾 **Prediction history using MySQL**
* 🌐 **Interactive React frontend**
* ☕ **Spring Boot REST backend**
* ⚡ **FastAPI machine-learning service**
* 🔗 **Communication between frontend, backend, and ML service**
* 🚀 **Deployment-ready architecture**

---

# 🧠 How XAI-Rumor Works

The system follows a multi-stage prediction pipeline.

```text
User enters social media text
            ↓
     React Frontend
            ↓
    Spring Boot Backend
            ↓
     FastAPI ML Service
            ↓
       Text Processing
            ↓
     BERT Embeddings
            ↓
    Random Forest Model
            ↓
   Rumor / Non-Rumor
            ↓
 Confidence & Probabilities
            ↓
     LIME Explanation
            ↓
    Spring Boot Backend
            ↓
      MySQL Database
            ↓
      React UI Result
```

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │    React Frontend    │
                    │      Vite            │
                    └──────────┬───────────┘
                               │
                               │ REST API
                               ▼
                    ┌──────────────────────┐
                    │   Spring Boot API    │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
                               │ HTTP Request
                               ▼
                    ┌──────────────────────┐
                    │   FastAPI ML Service │
                    │       Python         │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             ┌──────────────┐      ┌───────────────┐
             │     BERT     │      │ Random Forest │
             │  Embeddings  │─────▶│  Classifier   │
             └──────────────┘      └───────┬───────┘
                                           │
                                           ▼
                                    ┌─────────────┐
                                    │    LIME     │
                                    │ Explanation │
                                    └─────────────┘

                    Spring Boot Backend
                              │
                              ▼
                       ┌────────────┐
                       │   MySQL    │
                       │  Database  │
                       └────────────┘
```

---

# 🤖 Machine Learning Model

## BERT

XAI-Rumor uses:

```text
bert-base-uncased
```

BERT (**Bidirectional Encoder Representations from Transformers**) is used to generate contextual representations of the input text.

The generated BERT representation is then provided to the machine-learning classifier.

---

## 🌲 Random Forest

A **Random Forest classifier** is used for the final classification.

The classifier predicts one of two classes:

```text
Rumor
Non-Rumor
```

The trained Random Forest model is stored as:

```text
rumor_rf_model.joblib
```

---

# 🔍 Explainable AI with LIME

One of the main components of XAI-Rumor is **LIME**.

LIME stands for:

> Local Interpretable Model-Agnostic Explanations

A machine-learning model can produce a prediction without directly showing the user which parts of the input influenced that prediction.

LIME helps make an individual prediction more understandable by identifying words/features that contribute to the classification.

For example:

```text
Prediction: Rumor

Confidence: 51.67%

Important Features:
- viral
- claims
- government
- free
- official
```

The exact explanation depends on the input text and model output.

Therefore, XAI-Rumor provides both:

```text
Prediction
+
Explanation
```

rather than only displaying the classification result.

---

# 📊 Model Evaluation

The trained model was evaluated using a held-out test set from the project dataset.

| Metric    | Result |
| --------- | -----: |
| Accuracy  | 87.64% |
| Precision | 89.13% |
| Recall    | 87.23% |
| F1 Score  | 88.17% |

### Confusion Matrix

```text
                 Predicted
              Non-Rumor  Rumor

Actual
Non-Rumor        74        10
Rumor            12        82
```

These measurements are based on the project's dataset and test split. They should not be interpreted as guaranteed performance on unrelated real-world social-media content.

---

# 📚 Dataset

The project uses the **Ottawa shooting rumor dataset** for model development.

The dataset contains text samples and corresponding labels.

The classification labels used by the model are:

```text
non-rumor
rumor
```

The original dataset is **not included in this public repository**.

This is intentional because the dataset is excluded through `.gitignore`.

---

# 💻 Technology Stack

## Frontend

* React
* Vite
* JavaScript
* HTML5
* CSS3
* Axios

## Backend

* Java
* Spring Boot
* Spring Data JPA
* REST API
* Maven
* Jackson

## Machine Learning

* Python
* FastAPI
* Hugging Face Transformers
* BERT
* Scikit-learn
* Random Forest
* LIME
* Joblib

## Database

* MySQL
* Hibernate
* Spring Data JPA


# 📂 Project Structure

```text
XAI-Rumor/
│
├── RD-backend/
│   ├── src/
│   │   └── main/
│   │       ├── java/
│   │       │   └── com/
│   │       │       └── rumordetection/
│   │       │           └── backend/
│   │       │               ├── controller/
│   │       │               ├── entity/
│   │       │               ├── repository/
│   │       │               └── service/
│   │       │
│   │       └── resources/
│   │           └── application.properties
│   │
│   ├── pom.xml
│   ├── mvnw
│   └── mvnw.cmd
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── ml-service/
│   ├── app.py
│   ├── train_model.py
│   ├── requirements.txt
│   └── rumor_rf_model.joblib
│
├── .gitignore
└── README.md
```

---

# 🔄 Application Workflow

### 1. User Input

The user enters a social media post or text into the React application.

### 2. Frontend Request

React sends the text to the Spring Boot backend through a REST API.

### 3. Backend Communication

Spring Boot forwards the text to the FastAPI machine-learning service.

### 4. BERT Processing

The FastAPI service processes the text using BERT and generates contextual embeddings.

### 5. Classification

The embeddings are passed to the trained Random Forest model.

### 6. Prediction

The model generates:

* Rumor / Non-Rumor result
* Confidence
* Rumor probability
* Non-Rumor probability

### 7. Explanation

LIME generates an explanation for the individual prediction.

### 8. Database

Prediction information can be stored in MySQL for history management.

### 9. Result Display

The React frontend displays the prediction and explanation to the user.

---

# 🔗 API

## Spring Boot Prediction API

```http
POST /api/predictions
```

Example request:

```json
{
  "text": "A viral social media post claims that the government will give every citizen 50,000 rupees for free, but no official announcement has been made."
}
```

---

## FastAPI Prediction API

```http
POST /predict
```

The ML service returns prediction information such as:

```json
{
  "result": "Rumor",
  "confidence": 0.5166666666666667,
  "rumor_probability": 0.5166666666666667,
  "non_rumor_probability": 0.48333333333333334,
  "lime_explanation": []
}
```

The LIME explanation is generated based on the individual input.

---

# 🗄️ Database & History

The Spring Boot backend uses MySQL for storing prediction history.

The prediction record can include information such as:

* Input text
* Prediction result
* Confidence
* LIME explanation
* Timestamp

This allows the application to maintain and display previous prediction results.

---

# ⚙️ Running the Project Locally

## Prerequisites

Install:

* Python 3.x
* Java 21
* Node.js
* npm
* MySQL
* Git

---

## 1️⃣ Start the ML Service

Open a terminal:

```bash
cd ml-service
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
python -m uvicorn app:app --reload --port 8001
```

ML service:

```text
http://127.0.0.1:8001
```

---

## 2️⃣ Start the Spring Boot Backend

Open another terminal:

```powershell
cd RD-backend
```

Run:

```powershell
.\mvnw.cmd spring-boot:run
```

Backend:

```text
http://localhost:8081
```

Make sure MySQL is running and the required database configuration is available.

---

## 3️⃣ Start the React Frontend

Open another terminal:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start the application:

```powershell
npm run dev
```

Vite will display the frontend URL in the terminal.

---

# 🌐 Deployment Architecture

The project is designed to be deployed as separate services.

```text
                    ┌─────────────────┐
                    │ React Frontend  │
                    │ Render / Vercel │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Spring Boot API │
                    │     Render      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ FastAPI ML API  │
                    │     Render      │
                    └────────┬────────┘
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
                BERT              Random Forest
                  │                     │
                  └──────────┬──────────┘
                             ▼
                           LIME

                    Spring Boot
                         │
                         ▼
                    Cloud MySQL
```

---

# 🔐 Configuration

The application supports environment-based configuration for deployment.

Important backend configuration includes:

```text
DB_URL
DB_USERNAME
DB_PASSWORD
ML_SERVICE_URL
```

Sensitive credentials should be provided through environment variables rather than committed to the repository.

---

# 🚀 Future Enhancements

Potential future improvements include:

* Multilingual rumor detection
* Larger and more diverse datasets
* Improved model calibration
* Additional transformer-based models
* Integration with fact-checking sources
* Real-time social-media monitoring
* Advanced prediction analytics
* Improved LIME visualization
* Automated model retraining
* User authentication and authorization
* Cloud database integration
* Production monitoring and logging

---

# 🎓 Academic & Research Context

XAI-Rumor demonstrates the integration of multiple areas of computer science:

* Natural Language Processing
* Transformer Models
* Machine Learning
* Explainable Artificial Intelligence
* Full-Stack Development
* REST API Development
* Database Management
* Cloud Deployment

The project demonstrates how an AI model can be integrated into a complete web-based application while providing an explanation for individual predictions.

---

# 👩‍💻 Developer

## Rajeswaree Nath

**B.Tech – Computer Science and Engineering**

Aspiring Software Engineer | AI/ML & Full-Stack Development

GitHub:
https://github.com/nathrajeswaree26-netizen

LinkedIn:
https://www.linkedin.com/in/rajeswaree-nath/

---

# 📌 Important Note

XAI-Rumor is an academic and research-oriented project.

A model prediction should not be treated as definitive proof that information is true or false. Actual verification of information should be performed using reliable sources, evidence, and appropriate fact-checking procedures.

---

## ⭐ Project

If you find XAI-Rumor useful for learning about **NLP, Machine Learning, Explainable AI, or full-stack AI application development**, feel free to explore the repository and contribute ideas for improvement.
