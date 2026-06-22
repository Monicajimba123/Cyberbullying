from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# =========================
# LOAD MODEL + VECTORIZER ONCE (IMPORTANT FIX)
# =========================
try:
    model = joblib.load("cyberbullying_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    print("✅ Model + Vectorizer loaded successfully")
except Exception as e:
    model = None
    vectorizer = None
    print("❌ Loading failed:", str(e))


# =========================
# ROOT ROUTE
# =========================
@app.route("/")
def home():
    return "Cyberbullying API is running 🚀"


# =========================
# PREDICT ROUTE
# =========================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        if model is None or vectorizer is None:
            return jsonify({"error": "Model or Vectorizer not loaded"}), 500

        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' field"}), 400

        text = data["text"]

        # Convert text → vector
        text_vec = vectorizer.transform([text])

        # Predict
        prediction = model.predict(text_vec)[0]

        return jsonify({
            "label": prediction,
            "input": text
        })

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({
            "error": str(e)
        }), 500


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )