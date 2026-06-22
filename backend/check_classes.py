import joblib

model = joblib.load("cyberbullying_model.pkl")

print("Classes:", model.classes_)