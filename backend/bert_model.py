import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "unitary/toxic-bert"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=1)

    label_id = torch.argmax(probs).item()

    labels = ["non-toxic", "toxic"]

    return labels[label_id], float(probs.max())

if __name__ == "__main__":
    while True:
        text = input("Enter text: ")
        label, confidence = predict(text)
        print(f"Prediction: {label} ({confidence:.2f})")