import { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState("");

  const checkText = () => {
    const badWords = ["stupid", "idiot", "hate", "ugly"];

    const lowerText = text.toLowerCase();

    const isToxic = badWords.some(word => lowerText.includes(word));

    if (isToxic) {
      setResult("⚠️ Toxic / Cyberbullying Detected");
    } else {
      setResult("✅ Safe Message");
    }
  };

  return (
    <div style={{ padding: "15px", fontFamily: "Arial", width: "250px" }}>
      <h3>Cyberbullying Detector</h3>

      <textarea
        rows="4"
        style={{ width: "100%" }}
        placeholder="Type message..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button onClick={checkText} style={{ marginTop: "10px" }}>
        Analyze
      </button>

      <p style={{ marginTop: "10px", fontWeight: "bold" }}>
        {result}
      </p>
    </div>
  );
}

export default App;