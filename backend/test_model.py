import joblib
import re

# =========================
# LOAD MODEL
# =========================
model = joblib.load("cyberbullying_model.pkl")

# =========================
# SAME CLEANING FUNCTION
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

# =========================
# TEST MODE
# =========================
print("\n🔥 Cyberbullying Detector Test Mode\n")

while True:
    text = input("Enter text: ")

    if text.lower() == "exit":
        break

    cleaned = clean_text(text)
    prediction = model.predict([cleaned])[0]

    print("Prediction:", prediction)