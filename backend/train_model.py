import pandas as pd
import re
import string

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

# =========================
# Load dataset
# =========================
df = pd.read_csv("dataset/final_hateXplain.csv")

# =========================
# Better cleaning function
# =========================
def clean_text(text):
    text = str(text).lower()

    # remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # remove mentions
    text = re.sub(r"@\w+", "", text)

    # remove hashtags symbol only
    text = re.sub(r"#", "", text)

    # remove numbers (helps reduce noise)
    text = re.sub(r"\d+", "", text)

    # remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# Apply cleaning
df["comment"] = df["comment"].apply(clean_text)

# =========================
# Features & labels
# =========================
X = df["comment"]
y = df["label"]

# =========================
# Train-test split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =========================
# Compute class weights (IMPORTANT IMPROVEMENT)
# =========================
classes = np.unique(y_train)
weights = compute_class_weight(class_weight="balanced", classes=classes, y=y_train)
class_weight_dict = dict(zip(classes, weights))

# =========================
# Stronger model pipeline
# =========================
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        analyzer="char_wb",       # strong for slang + spelling variations
        ngram_range=(2, 5),       # better context than (1,3)
        max_features=120000,
        min_df=2,
        sublinear_tf=True
    )),

    ("clf", LinearSVC(
        C=1.5,
        class_weight=class_weight_dict
    ))
])

# =========================
# Train
# =========================
model.fit(X_train, y_train)

# =========================
# Predict
# =========================
y_pred = model.predict(X_test)

# =========================
# Results
# =========================
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))