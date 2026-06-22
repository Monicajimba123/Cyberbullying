export async function analyzeText(text) {
  try {
    const res = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text })
    });

    const data = await res.json();

    console.log("STATUS:", res.status);
    console.log("API RESPONSE:", data);

    // ❗ DON'T hide backend errors
    if (data.error) {
      return "backend_error: " + data.error;
    }

    if (!data.label) {
      return "no_label_returned";
    }

    return data.label;

  } catch (error) {
    console.error("API Error:", error);
    return "network_error";
  }
}