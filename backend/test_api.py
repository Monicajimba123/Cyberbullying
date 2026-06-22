import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "text": "you are stupid"
}

res = requests.post(url, json=data)

print(res.status_code)
print(res.json())