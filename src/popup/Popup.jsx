import { useState } from "react";
import { analyzeText } from "../utils/api";
import "./popup.css";

export default function Popup() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!text.trim()) return;

    setLoading(true);

    try {
      const response = await analyzeText(text);
      setResult(response.prediction);
    } catch (error) {
      console.error(error);
      setResult("error");
    }

    setLoading(false);
  };

  const getResultLabel = () => {
    if (!result) return "";

    switch (result.toLowerCase()) {
      case "normal":
        return "✅ Normal Content";

      case "offensive":
        return "⚠️ Offensive Content";

      case "hatespeech":
        return "🚫 Hate Speech";

      default:
        return "❌ Error";
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

        <button onClick={handleAnalyze}>
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