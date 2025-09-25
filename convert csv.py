import pandas as pd

# Baca file Excel
df = pd.read_excel("all.xlsx")

# Simpan ke CSV
df.to_csv("data.csv", index=False)
