from fastapi import FastAPI
from pydantic import BaseModel

from transformers import BertTokenizer, BertModel

import torch
import joblib
import re
import os
import numpy as np

from lime.lime_text import LimeTextExplainer


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="Rumor Detection ML Service",
    description="BERT + Random Forest + LIME Explainability",
    version="2.0.0"
)


# ============================================================
# Request / Response Models
# ============================================================

class PredictionRequest(BaseModel):
    text: str


class LimeExplanation(BaseModel):
    word: str
    weight: float


class PredictionResponse(BaseModel):
    result: str
    confidence: float
    rumor_probability: float
    non_rumor_probability: float
    lime_explanation: list[LimeExplanation]


# ============================================================
# Device
# ============================================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("========================================")
print("Using device:", device)
print("========================================")


# ============================================================
# BERT
# ============================================================

MODEL_NAME = "bert-base-uncased"

print("Loading BERT tokenizer...")

tokenizer = BertTokenizer.from_pretrained(
    MODEL_NAME
)

print("Loading BERT model...")

bert_model = BertModel.from_pretrained(
    MODEL_NAME
)

bert_model = bert_model.to(device)

bert_model.eval()

print("BERT loaded successfully!")


# ============================================================
# Random Forest
# ============================================================

RF_MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "rumor_rf_model.joblib"
)

print("========================================")
print("Loading Random Forest...")
print("Model path:", RF_MODEL_PATH)
print("========================================")

if not os.path.exists(RF_MODEL_PATH):
    raise FileNotFoundError(
        f"Random Forest model not found: {RF_MODEL_PATH}"
    )

rf_model = joblib.load(
    RF_MODEL_PATH
)

print("Random Forest loaded successfully!")
print("Random Forest classes:", rf_model.classes_)

if hasattr(rf_model, "n_features_in_"):
    print(
        "Expected number of features:",
        rf_model.n_features_in_
    )

print("========================================")


# ============================================================
# Verify Model
# ============================================================

if len(rf_model.classes_) < 2:
    raise RuntimeError(
        "ERROR: Random Forest contains only one class. "
        "The model must be trained using BOTH Rumor and Non-Rumor examples."
    )


# ============================================================
# LIME
# ============================================================

class_names = [
    str(class_name)
    for class_name in rf_model.classes_
]

explainer = LimeTextExplainer(
    class_names=class_names
)

print("LIME loaded successfully!")
print("LIME classes:", class_names)


# ============================================================
# Stopwords
# ============================================================

try:

    import nltk
    from nltk.corpus import stopwords

    try:

        stop_words = set(
            stopwords.words("english")
        )

    except LookupError:

        nltk.download("stopwords")

        stop_words = set(
            stopwords.words("english")
        )

except Exception:

    stop_words = set()


# ============================================================
# Text Cleaning
# ============================================================

def clean_text(text: str) -> str:

    text = str(text).lower()

    # Remove URLs
    text = re.sub(
        r"http\S+|www\S+",
        "",
        text
    )

    # Remove mentions
    text = re.sub(
        r"@\w+",
        "",
        text
    )

    # Remove hashtags but keep the word
    text = re.sub(
        r"#(\w+)",
        r"\1",
        text
    )

    # Keep English letters and spaces
    text = re.sub(
        r"[^a-z\s]",
        " ",
        text
    )

    # Normalize spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# ============================================================
# BERT Embedding
# ============================================================

def get_bert_embedding(text: str):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }

    with torch.no_grad():

        outputs = bert_model(
            **inputs
        )

    # Mean pooling
    embedding = (
        outputs.last_hidden_state
        .mean(dim=1)
        .squeeze(0)
        .cpu()
        .numpy()
    )

    return embedding.astype(
        np.float32
    )


# ============================================================
# LIME Prediction Function
# ============================================================

def predict_proba_for_lime(texts):

    embeddings = []

    for text in texts:

        cleaned = clean_text(text)

        if not cleaned.strip():
            cleaned = "unknown"

        embedding = get_bert_embedding(
            cleaned
        )

        embeddings.append(
            embedding
        )

    embeddings = np.asarray(
        embeddings,
        dtype=np.float32
    )

    probabilities = rf_model.predict_proba(
        embeddings
    )

    return probabilities


# ============================================================
# Get Class Probabilities
# ============================================================

def get_class_probabilities(probabilities):

    rumor_probability = 0.0
    non_rumor_probability = 0.0

    classes = list(
        rf_model.classes_
    )

    for class_name, probability in zip(
        classes,
        probabilities
    ):

        class_string = str(
            class_name
        ).strip().lower()

        probability = float(
            probability
        )

        # Rumor labels
        if class_string in [
            "rumor",
            "rumour",
            "1",
            "true"
        ]:

            rumor_probability = probability

        # Non-rumor labels
        elif class_string in [
            "non-rumor",
            "non rumor",
            "non_rumor",
            "non-rumour",
            "non rumour",
            "0",
            "false"
        ]:

            non_rumor_probability = probability

    # ========================================================
    # Unknown label fallback
    # ========================================================

    if (
        rumor_probability == 0.0
        and
        non_rumor_probability == 0.0
    ):

        print(
            "WARNING: Unknown class labels:",
            classes
        )

        if len(probabilities) >= 2:

            non_rumor_probability = float(
                probabilities[0]
            )

            rumor_probability = float(
                probabilities[1]
            )

    return (
        rumor_probability,
        non_rumor_probability
    )


# ============================================================
# Root
# ============================================================

@app.get("/")
def root():

    return {
        "message": "Rumor Detection ML Service is running",
        "model": "BERT + Random Forest",
        "classes": [
            str(c)
            for c in rf_model.classes_
        ]
    }


# ============================================================
# Health
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "UP",
        "bert": "loaded",
        "random_forest": "loaded",
        "lime": "loaded",
        "classes": [
            str(c)
            for c in rf_model.classes_
        ]
    }


# ============================================================
# Prediction
# ============================================================

@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(
    request: PredictionRequest
):

    # ========================================================
    # Original text
    # ========================================================

    original_text = request.text.strip()

    if not original_text:

        return PredictionResponse(
            result="INVALID",
            confidence=0.0,
            rumor_probability=0.0,
            non_rumor_probability=0.0,
            lime_explanation=[]
        )

    print("\n")
    print("========================================")
    print("NEW PREDICTION REQUEST")
    print("========================================")

    print(
        "Original text:",
        original_text
    )


    # ========================================================
    # Clean text
    # ========================================================

    cleaned_text = clean_text(
        original_text
    )

    if not cleaned_text.strip():

        cleaned_text = "unknown"

    print(
        "Cleaned text:",
        cleaned_text
    )


    # ========================================================
    # BERT
    # ========================================================

    embedding = get_bert_embedding(
        cleaned_text
    )

    embedding = embedding.reshape(
        1,
        -1
    )

    print(
        "Embedding shape:",
        embedding.shape
    )


    # ========================================================
    # Random Forest Prediction
    # ========================================================

    prediction = rf_model.predict(
        embedding
    )[0]

    probabilities = rf_model.predict_proba(
        embedding
    )[0]

    classes = list(
        rf_model.classes_
    )


    # ========================================================
    # IMPORTANT DEBUG INFORMATION
    # ========================================================

    print("========================================")
    print("DEBUG - RANDOM FOREST")
    print("========================================")

    print(
        "Input embedding shape:",
        embedding.shape
    )

    print(
        "RF classes:",
        rf_model.classes_
    )

    print(
        "RF raw prediction:",
        prediction
    )

    print(
        "RF probabilities:",
        probabilities
    )

    print("")

    for class_name, probability in zip(
        classes,
        probabilities
    ):

        print(
            f"Class: {class_name} "
            f"Probability: {float(probability):.6f}"
        )

    print("========================================")


    # ========================================================
    # Convert probabilities
    # ========================================================

    (
        rumor_probability,
        non_rumor_probability
    ) = get_class_probabilities(
        probabilities
    )


    # ========================================================
    # Final result
    # ========================================================

    prediction_string = str(
        prediction
    ).strip().lower()


    if prediction_string in [
        "rumor",
        "rumour"
    ]:

        result = "Rumor"


    elif prediction_string in [
        "non-rumor",
        "non rumor",
        "non_rumor",
        "non-rumour",
        "non rumour"
    ]:

        result = "Non-Rumor"


    elif prediction_string == "1":

        result = "Rumor"


    elif prediction_string == "0":

        result = "Non-Rumor"


    else:

        # Unknown label:
        # choose using probability

        if rumor_probability >= non_rumor_probability:

            result = "Rumor"

        else:

            result = "Non-Rumor"


    # ========================================================
    # Confidence
    # ========================================================

    if result == "Rumor":

        confidence = rumor_probability

    else:

        confidence = non_rumor_probability


    print("========================================")
    print("FINAL CLASSIFICATION")
    print("========================================")

    print(
        "Prediction:",
        result
    )

    print(
        "Rumor probability:",
        rumor_probability
    )

    print(
        "Non-Rumor probability:",
        non_rumor_probability
    )

    print(
        "Confidence:",
        confidence
    )

    print("========================================")


    # ========================================================
    # LIME
    # ========================================================

    lime_list = []

    try:

        rf_classes = list(
            rf_model.classes_
        )

        predicted_class_index = rf_classes.index(
            prediction
        )

        print(
            "Predicted class index:",
            predicted_class_index
        )

        print(
            "Generating LIME explanation..."
        )

        explanation = explainer.explain_instance(
            original_text,
            predict_proba_for_lime,
            labels=tuple(
                range(
                    len(rf_classes)
                )
            ),
            num_features=10,
            num_samples=100
        )

        print(
            "LIME local_exp keys:",
            list(
                explanation.local_exp.keys()
            )
        )


        if predicted_class_index in explanation.local_exp:

            explanation_items = (
                explanation.local_exp[
                    predicted_class_index
                ]
            )

            print(
                "Found explanation items:",
                explanation_items
            )

            for feature_id, weight in explanation_items:

                word = (
                    explanation
                    .domain_mapper
                    .indexed_string
                    .word(feature_id)
                )

                lime_list.append(
                    LimeExplanation(
                        word=str(word),
                        weight=float(weight)
                    )
                )


        lime_list = lime_list[:10]

        print(
            "LIME explanation:",
            lime_list
        )


    except Exception as e:

        print("========================================")
        print("LIME ERROR")
        print(
            "Type:",
            type(e).__name__
        )
        print(
            "Error:",
            repr(e)
        )
        print("========================================")

        lime_list = []


    # ========================================================
    # Final response
    # ========================================================

    print("========================================")
    print("FINAL RESULT:", result)

    print(
        "FINAL CONFIDENCE:",
        confidence
    )

    print(
        "NUMBER OF LIME FEATURES:",
        len(lime_list)
    )

    print("========================================")
    print()


    return PredictionResponse(
        result=result,
        confidence=float(confidence),
        rumor_probability=float(
            rumor_probability
        ),
        non_rumor_probability=float(
            non_rumor_probability
        ),
        lime_explanation=lime_list
    )