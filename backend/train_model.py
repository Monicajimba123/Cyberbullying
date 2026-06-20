import pandas as pd
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils import resample

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv("dataset/Dataset.csv", encoding="latin1")

# Drop empty rows
df = df.dropna(subset=["comment", "label"])

# =========================
# CLEAN LABELS (VERY IMPORTANT)
# =========================
df["label"] = df["label"].astype(str).str.lower().str.strip()

df["label"] = df["label"].replace({
    "0": "normal",
    "1": "toxic",
    "non-toxic": "normal",
    "not toxic": "normal",
    "hate": "toxic",
    "offensive": "toxic",
    "abusive": "toxic"
})

# Remove unknown labels
df = df[df["label"].isin(["normal", "toxic"])]

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

df["comment"] = df["comment"].apply(clean_text)

# Remove very short noise
df = df[df["comment"].str.len() > 3]

# =========================
# BALANCE DATASET (KEY FIX)
# =========================
major = df[df.label == "normal"]
minor = df[df.label == "toxic"]

minor_up = resample(
    minor,
    replace=True,
    n_samples=len(major),
    random_state=42
)

df = pd.concat([major, minor_up])
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# =========================
# FEATURES & LABELS
# =========================
X = df["comment"]
y = df["label"]

# =========================
# SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =========================
# TF-IDF (OPTIMIZED)
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
# STRONG MODEL
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

# =========================
# MANUAL TEST MODE
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