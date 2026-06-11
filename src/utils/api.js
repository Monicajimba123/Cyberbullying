export async function analyzeText(text) {
  // Simple rule-based demo (replace with real AI later)

  const badWords = ["idiot", "stupid", "hate", "kill", "ugly"];

  const lowerText = text.toLowerCase();

  for (let word of badWords) {
    if (lowerText.includes(word)) {
      return "⚠️ Cyberbullying Detected";
    }
  }

  return "✅ Safe Content";
}