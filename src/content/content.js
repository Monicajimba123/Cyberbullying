chrome.runtime.onMessage.addListener((message) => {
  if (message.type === "ANALYSIS_RESULT") {
    const { toxic, score } = message.payload;

    if (toxic) {
      showWarning(score);
    }
  }
});

function showWarning(score) {
  const warning = document.createElement("div");

  warning.innerText = `⚠️ Warning: Toxic content detected (score: ${score.toFixed(
    2
  )})`;

  warning.style.position = "fixed";
  warning.style.bottom = "20px";
  warning.style.right = "20px";
  warning.style.background = "red";
  warning.style.color = "white";
  warning.style.padding = "10px";
  warning.style.zIndex = 999999;

  document.body.appendChild(warning);

  setTimeout(() => warning.remove(), 5000);
}
console.log("Cyberbullying detector running...");