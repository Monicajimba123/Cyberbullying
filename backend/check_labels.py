import pandas as pd

df = pd.read_csv("dataset/Dataset.csv", encoding="latin1")

print(df["label"].value_counts())