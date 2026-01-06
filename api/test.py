import pandas as pd

df = pd.read_csv("/Users/matthewlu/Documents/Projects/sports-scraper/api/uploads/NBA Full Stat Detail.csv")
df = df[df["Scenario"] == "Default"]
df = df.set_index('Player')
print(df["Scenario"].unique())
print(df.index.duplicated().sum())