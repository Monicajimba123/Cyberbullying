// background.js

chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  if (message.type === "ANALYZE_TEXT") {
    const text = message.payload;

    const result = await analyzeToxicity(text);

    // send result back to content script
    chrome.tabs.sendMessage(sender.tab.id, {
      type: "ANALYSIS_RESULT",
      payload: result,
    });
  }
});

// Dummy AI function (replace later with real API)
async function analyzeToxicity(text) {
  const toxicWords = ["hate", "stupid", "idiot", "kill"];

  let score = 0;

  toxicWords.forEach((word) => {
    if (text.toLowerCase().includes(word)) {
      score += 0.3;
    }
  });

  return {
    toxic: score > 0.5,
    score,
  };
}