import pandas as pd

df = pd.read_csv("cry.csv", sep=None, engine="python")
print(df.head())
