import { useState } from "react";
import { analyzeText } from "../utils/api";
import "./popup.css";

export default function Popup() {
  const [text, setText] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!text.trim()) {
      alert("Please enter some text");
      return;
    }

    setLoading(true);

    try {
      const response = await analyzeText(text);

      console.log("API RESPONSE:", response);

      // ✅ FIX: backend returns STRING, not object
      if (!response || response === "error") {
        setResult("error");
      } else {
        setResult(response);
      }

    } catch (error) {
      console.error("Popup Error:", error);
      setResult("error");
    }

    setLoading(false);
  };

  const getResultLabel = () => {
    if (!result) return "";

    switch (result.toLowerCase()) {
      case "normal":
        return "✅ Normal Content";

      case "toxic":
        return "⚠️ Toxic Content";

      case "hatespeech":
      case "hate speech":
        return "🚫 Hate Speech";

      case "error":
        return "❌ Error occurred";

      default:
        return `Prediction: ${result}`;
    }
  };

  return (
    <div className="container">
      <div className="card">
        <div className="header">
          <h1>🛡 Cyberbullying Detection</h1>
          <p>AI-Powered Content Analysis System</p>
        </div>

        <textarea
          placeholder="Type or paste text for analysis..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button onClick={handleAnalyze} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Text"}
        </button>

        {result && (
          <div className={`result ${result.toLowerCase()}`}>
            <h3>{getResultLabel()}</h3>
          </div>
        )}

        <div className="footer">
          <small>Cyberbullying Detection v1.0</small>
        </div>
      </div>
    </div>
  );
}