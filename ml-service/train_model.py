import os
import joblib
import numpy as np
import pandas as pd
import torch

from transformers import BertTokenizer, BertModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# 1. SETTINGS
# ============================================================

DATASET_PATH = "ottawashooting.xlsx"
MODEL_OUTPUT = "rumor_rf_model.joblib"

BERT_MODEL_NAME = "bert-base-uncased"

RANDOM_STATE = 42


# ============================================================
# 2. CHECK DATASET
# ============================================================

if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(
        f"Dataset not found: {DATASET_PATH}\n"
        "Make sure ottawashooting.xlsx is inside the ml-service folder."
    )

print("Loading dataset...")

df = pd.read_excel(DATASET_PATH)

print("\nDataset shape:", df.shape)
print("Columns:", df.columns.tolist())


# ============================================================
# 3. CHECK REQUIRED COLUMNS
# ============================================================

if "Text" not in df.columns:
    raise ValueError("Dataset must contain a 'Text' column.")

if "Label" not in df.columns:
    raise ValueError("Dataset must contain a 'Label' column.")


# ============================================================
# 4. CLEAN DATA
# ============================================================

df = df[["Text", "Label"]].copy()

df["Text"] = df["Text"].fillna("").astype(str).str.strip()
df["Label"] = df["Label"].astype(str).str.strip().str.lower()

# Remove empty texts
df = df[df["Text"] != ""]

# Keep only expected labels
df = df[df["Label"].isin(["rumor", "non-rumor"])]

# Remove duplicate rows
df = df.drop_duplicates()

print("\nAfter cleaning:")
print("Number of records:", len(df))

print("\nLabel distribution:")
print(df["Label"].value_counts())


# ============================================================
# 5. LOAD BERT
# ============================================================

print("\nLoading BERT...")

tokenizer = BertTokenizer.from_pretrained(BERT_MODEL_NAME)
bert_model = BertModel.from_pretrained(BERT_MODEL_NAME)

bert_model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Device:", device)

bert_model.to(device)


# ============================================================
# 6. CREATE BERT EMBEDDINGS
# ============================================================

def create_embeddings(texts, batch_size=16):

    all_embeddings = []

    for start in range(0, len(texts), batch_size):

        batch_texts = texts[start:start + batch_size]

        inputs = tokenizer(
            batch_texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=128
        )

        inputs = {
            key: value.to(device)
            for key, value in inputs.items()
        }

        with torch.no_grad():

            outputs = bert_model(**inputs)

            # Same mean-pooling approach used by app.py
            embeddings = outputs.last_hidden_state.mean(dim=1)

        all_embeddings.append(
            embeddings.cpu().numpy()
        )

        print(
            f"Processed {min(start + batch_size, len(texts))}"
            f"/{len(texts)}"
        )

    return np.vstack(all_embeddings)


# ============================================================
# 7. GENERATE EMBEDDINGS
# ============================================================

print("\nGenerating BERT embeddings...")

texts = df["Text"].tolist()

X = create_embeddings(texts)

print("\nEmbedding shape:", X.shape)


# ============================================================
# 8. CREATE LABELS
# ============================================================

y = df["Label"].values


# ============================================================
# 9. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# 10. TRAIN RANDOM FOREST
# ============================================================

print("\nTraining Random Forest...")

rf_model = RandomForestClassifier(
    n_estimators=300,
    random_state=RANDOM_STATE,
    class_weight="balanced",
    n_jobs=-1
)

rf_model.fit(X_train, y_train)


# ============================================================
# 11. PREDICTION
# ============================================================

y_pred = rf_model.predict(X_test)


# ============================================================
# 12. EVALUATION
# ============================================================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    pos_label="rumor"
)

recall = recall_score(
    y_test,
    y_pred,
    pos_label="rumor"
)

f1 = f1_score(
    y_test,
    y_pred,
    pos_label="rumor"
)


print("\n")
print("=" * 60)
print("MODEL EVALUATION")
print("=" * 60)

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        labels=["non-rumor", "rumor"]
    )
)

print("Confusion Matrix:")
print(
    confusion_matrix(
        y_test,
        y_pred,
        labels=["non-rumor", "rumor"]
    )
)


# ============================================================
# 13. SAVE MODEL
# ============================================================

print("\nSaving model...")

joblib.dump(
    rf_model,
    MODEL_OUTPUT
)

print("\nModel saved successfully:")
print(MODEL_OUTPUT)

print("\nClasses:", rf_model.classes_)
print("Features:", rf_model.n_features_in_)
print("Trees:", len(rf_model.estimators_))

print("\nTraining completed successfully!")