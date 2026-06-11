import { useState } from "react";
import { analyzeText } from "../utils/api";

export default function Popup() {
  const [text, setText] = useState("");
  const [result, setResult] = useState("");

  const handleCheck = async () => {
    const response = await analyzeText(text);
    setResult(response);
  };

  return (
    <div style={{ width: "300px", padding: "10px" }}>
      <h2>Cyberbullying Detector</h2>

      <textarea
        rows="5"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste text here..."
        style={{ width: "100%" }}
      />

      <button onClick={handleCheck}>
        Check
      </button>

      <p><b>Result:</b> {result}</p>
    </div>
  );
}