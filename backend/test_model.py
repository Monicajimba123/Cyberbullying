import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report

# CHANGE THIS if your dataset file name is different
df = pd.read_csv("dataset/final_hateXplain.csv")

X = df["comment"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1,2),
    max_features=30000
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LinearSVC(class_weight="balanced")
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)

print("\n🎯 Accuracy:", accuracy_score(y_test, y_pred))

print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred))
print("\n🔥 Manual Testing Mode (type 'exit' to quit)\n")

while True:
    text = input("Enter text: ")

    if text.lower() == "exit":
        break

    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)

    print("Prediction:", prediction[0])