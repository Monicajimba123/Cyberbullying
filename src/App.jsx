import { useState } from "react";
import { analyzeText } from "./utils/api";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState("");
  const [score, setScore] = useState(0);
  const [words, setWords] = useState([]);

  const checkText = async () => {
    try {
      const response = await analyzeText(text);

      const prediction = response.prediction;

      setResult(prediction);

      let calculatedScore = 0;

      if (prediction === "Safe Message") calculatedScore = 0;
      else if (prediction === "Low Risk") calculatedScore = 30;
      else if (prediction === "Medium Risk") calculatedScore = 60;
      else calculatedScore = 90;

      setScore(calculatedScore);
      setWords([]);

    } catch (error) {
      console.error("Error:", error);
      setResult("Error");
      setScore(0);
      setWords([]);
    }
  };

  const getColor = () => {
    if (score === 0) return "#2ecc71";
    if (score <= 50) return "#f1c40f";
    if (score <= 75) return "#e67e22";
    return "#e74c3c";
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>

        <h1 style={styles.title}>Cyberbullying Detector</h1>
        <p style={styles.subtitle}>
          AI-powered text safety analysis system
        </p>

        <textarea
          style={styles.textarea}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type a message to analyze..."
        />

        <button style={styles.button} onClick={checkText}>
          Analyze Text
        </button>

        <div style={styles.resultBox}>
          <h2 style={{ color: getColor(), marginBottom: "10px" }}>
            {result}
          </h2>

          <div style={styles.barBackground}>
            <div
              style={{
                ...styles.barFill,
                width: `${score}%`,
                backgroundColor: getColor()
              }}
            />
          </div>

          <p style={styles.scoreText}>
            Toxicity Score: <b>{score}%</b>
          </p>

          <div style={styles.section}>
            <h4>Detected Words</h4>
            {words.length > 0 ? (
              <div style={styles.tags}>
                {words.map((w, i) => (
                  <span key={i} style={styles.tag}>{w}</span>
                ))}
              </div>
            ) : (
              <p style={{ color: "#888" }}>No harmful words detected</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(135deg, #0f172a, #1e293b)",
    fontFamily: "Segoe UI, sans-serif",
    padding: "20px"
  },

  card: {
    width: "480px",
    background: "#ffffff",
    borderRadius: "16px",
    padding: "30px",
    boxShadow: "0 20px 50px rgba(0,0,0,0.25)",
    textAlign: "center"
  },

  title: {
    margin: "0",
    fontSize: "26px",
    fontWeight: "700",
    color: "#111827"
  },

  subtitle: {
    marginTop: "6px",
    marginBottom: "20px",
    fontSize: "13px",
    color: "#6b7280"
  },

  textarea: {
    width: "100%",
    height: "120px",
    padding: "12px",
    borderRadius: "10px",
    border: "1px solid #d1d5db",
    outline: "none",
    fontSize: "14px",
    resize: "none",
    marginBottom: "12px"
  },

  button: {
    width: "100%",
    padding: "12px",
    border: "none",
    borderRadius: "10px",
    background: "#2563eb",
    color: "white",
    fontWeight: "600",
    cursor: "pointer"
  },

  resultBox: {
    marginTop: "20px",
    textAlign: "left"
  },

  barBackground: {
    width: "100%",
    height: "10px",
    background: "#e5e7eb",
    borderRadius: "20px",
    overflow: "hidden",
    marginTop: "10px"
  },

  barFill: {
    height: "100%",
    borderRadius: "20px",
    transition: "width 0.4s ease"
  },

  scoreText: {
    marginTop: "10px",
    fontSize: "14px",
    color: "#374151"
  },

  section: {
    marginTop: "15px"
  },

  tags: {
    display: "flex",
    flexWrap: "wrap",
    gap: "6px"
  },

  tag: {
    background: "#fee2e2",
    color: "#991b1b",
    padding: "5px 10px",
    borderRadius: "20px",
    fontSize: "12px"
  }
};

export default App;