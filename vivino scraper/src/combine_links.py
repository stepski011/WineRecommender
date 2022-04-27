import pandas as pd
import pathlib
import os

filePath = pathlib.Path(__file__).parent.resolve()
dfList = []

files = os.listdir(str(filePath)+"/../temp/product_detail_links/")
for file in files:
    temp_df = pd.read_csv(
        str(filePath)+"/../temp/product_detail_links/"+file, index_col=False)
    dfList.append(temp_df)

df = pd.concat(dfList, ignore_index=True)

df = df.drop_duplicates("link")

try:
    df = df.drop(columns=["Unnamed: 0"])
except:
    pass
print(df.head())
df.to_csv(str(filePath)+"/../temp/wines_export.csv", index=False)
print("links combined!")
