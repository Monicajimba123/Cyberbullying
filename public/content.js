console.log("Cyberbullying extension running on page");

// Simple word list
const badWords = ["stupid", "idiot", "hate", "ugly"];

function scanPage() {
  const elements = document.querySelectorAll("p, span, div");

  elements.forEach((el) => {
    const text = el.innerText?.toLowerCase();

    if (!text) return;

    badWords.forEach((word) => {
      if (text.includes(word)) {
        el.style.backgroundColor = "red";
        el.style.color = "white";
      }
    });
  });
}

scanPage();