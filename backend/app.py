from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

# =========================
# LOAD MODEL
# =========================
model = joblib.load("cyberbullying_model.pkl")

# =========================
# ROOT CHECK
# =========================
@app.route("/")
def home():
    return "Cyberbullying API is running 🚀"

# =========================
# PREDICTION ENDPOINT
# =========================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Validate input
        if not data or "text" not in data:
            return jsonify({
                "error": "Missing 'text' field"
            }), 400

        text = data["text"]

        # Direct prediction (IMPORTANT: no extra preprocessing here)
        prediction = model.predict([text])[0]

        return jsonify({
            "input": text,
            "prediction": prediction
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)