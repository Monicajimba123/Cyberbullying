from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re

app = Flask(__name__)
CORS(app)

# Load model safely
model = joblib.load("cyberbullying_model.pkl")


# -------------------------
# Text Preprocessing
# -------------------------
def preprocess(text):
    text = str(text).lower()

    # remove links
    text = re.sub(r"http\S+", "", text)

    # remove special characters
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# -------------------------
# Test Route (IMPORTANT)
# -------------------------
@app.route("/")
def home():
    return "Backend is running 🚀"


# -------------------------
# Prediction Route
# -------------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "No text provided"}), 400

        text = data["text"]

        processed = preprocess(text)
        result = model.predict([processed])[0]

        return jsonify({
            "text": text,
            "prediction": str(result)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)