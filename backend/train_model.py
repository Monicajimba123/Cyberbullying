import pandas as pd
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report
import joblib

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv("dataset/Dataset.csv", encoding="latin1")

# =========================
# CLEAN COLUMN NAMES (CRITICAL FIX)
# =========================
df.columns = (
    df.columns
    .astype(str)
    .str.encode("utf-8", "ignore")
    .str.decode("utf-8")
    .str.strip()
    .str.lower()
)

print("\n📌 CLEAN COLUMNS:", list(df.columns))

# Ensure required columns exist
if "comment" not in df.columns or "label" not in df.columns:
    raise Exception(f"Missing columns. Found: {df.columns}")

text_col = "comment"
label_col = "label"

# Drop missing values
df = df.dropna(subset=[text_col, label_col])

# =========================
# CLEAN LABELS (3 CLASS FIX)
# =========================
df[label_col] = df[label_col].astype(str).str.lower().str.strip()

df[label_col] = df[label_col].replace({
    "0": "normal",
    "1": "toxic",
    "non-toxic": "normal",
    "not toxic": "normal",
    "offensive": "toxic",
    "abusive": "toxic",
    "hate": "hatespeech",
    "hatespeech": "hatespeech"
})

df = df[df[label_col].isin(["normal", "toxic", "hatespeech"])]

print("\n📊 Label distribution:\n", df[label_col].value_counts())

# =========================
# CLEAN TEXT
# =========================
def clean_text(text):
    text = str(text).lower()

    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text

df[text_col] = df[text_col].apply(clean_text)
df = df[df[text_col].str.len() > 3]

# =========================
# FIXED BALANCING (NO GROUPBY BUG)
# =========================
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# OPTIONAL: If you want mild balancing, uncomment this safe version:
"""
min_size = df[label_col].value_counts().min()
df = df.groupby(label_col, group_keys=False).apply(
    lambda x: x.sample(min_size, random_state=42)
)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
"""

# =========================
# FEATURES & LABELS
# =========================
X = df[text_col]
y = df[label_col]

# =========================
# TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =========================
# TF-IDF VECTOR
# =========================
vectorizer = TfidfVectorizer(
    analyzer="word",
    ngram_range=(1, 2),
    max_features=60000,
    min_df=2,
    stop_words="english",
    sublinear_tf=True
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# =========================
# MODEL TRAINING
# =========================
model = LinearSVC(
    C=0.8,
    class_weight="balanced"
)

model.fit(X_train_vec, y_train)

# =========================
# EVALUATION
# =========================
y_pred = model.predict(X_test_vec)

print("\n🎯 Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred))

print("\n📌 Classes learned:", model.classes_)

# =========================
# SAVE MODEL
# =========================
joblib.dump(model, "cyberbullying_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("\n✅ MODEL SAVED SUCCESSFULLY")

# =========================
# TEST MODE
# =========================
print("\n🔥 Manual Testing Mode (type 'exit' to quit)\n")

while True:
    text = input("Enter text: ")

    if text.lower() == "exit":
        break

    text = clean_text(text)
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)

    print("Prediction:", prediction[0])