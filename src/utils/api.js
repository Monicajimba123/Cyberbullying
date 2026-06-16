export async function analyzeText(text) {
  try {
    const res = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text })
    });

    if (!res.ok) {
      throw new Error("Server error");
    }

    const data = await res.json();
    return data;

  } catch (error) {
    console.error("API Error:", error);
    return { prediction: "Error" };
  }
}