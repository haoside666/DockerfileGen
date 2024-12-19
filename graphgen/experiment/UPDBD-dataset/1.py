import pandas as pd

df = pd.read_csv("./dockerfiles.csv")
print(set(df["repo_name"].tolist()))