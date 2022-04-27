# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 15:17:33 2022

@author: HP pc
"""

import pandas as pd
import json 
from sklearn.linear_model import LogisticRegression
import math

## read wine_data
with open("wine_data.json", mode="r", encoding="utf-8") as json_file:
    wine_data = json.load(json_file)
    
## Data frame for wine_data 
df = pd.DataFrame(wine_data)

df_taste = df[["wine_id","wine_tastes"]]


print(df_taste)
id = 0
dictList = []

for items in df_taste["wine_tastes"]:
    for k in items:

        taste_dict = {
             "wine_id" : int(df["wine_id"][id]),
             "flavor_name" : k["name"],
             "flavor_group" : k["group"],
             "flavor_count" : k["count"]

        }
        dictList.append(taste_dict)
    id += 1


for k in range(0,5):
    print(dictList[k])
    
    
# writing the datsa in json file 
data_file = open('flavor_wine_data.json', mode="w", encoding="utf-8" )
jsonString = json.dumps(dictList)

## print(df_dict)

## jsonString = json.dumps(df_dict)

data_file.write(jsonString)

data_file.close()
count = 0





