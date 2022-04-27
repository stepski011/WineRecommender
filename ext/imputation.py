# -*- coding: utf-8 -*-
"""
Regression imputation for predicting missing wine types

"""

import pandas as pd
import json 
from sklearn.linear_model import LogisticRegression
import math


#
def one_hot_encoding(row):
    
    """ Function takes in row of dataframe to convert each taste vector to representation of 0 and 1 """
    
    vector = [0] * len(all_tastes)
    for flavor in row["wine_tastes"]:
        try:
            i = all_tastes.index(flavor)
        except:
            i = all_tastes.index("Other")
        vector[i] = 1
    return vector


# function to assign label to the wine type
def label_encoding(row):
    
    """ Function assigns a label to each wine type"""

    if (row["wine_type"] == "red"):
        return 0
    if(row["wine_type"] == "white"):
        return 1
    return None


def get_prediction(row):
    
    """ Function takes in rows of dataframe and predicts missing labels for features """
    
    if (math.isnan(row["label"])):
        return clf.predict([row["features"]])
    return row["label"]


def label_decoding(row):
    
    """ Function adecodes lav=bel to a wine type"""
    
    if (int(row["label"]) == 0):
        return "red"
    if(int(row["label"]) == 1):
        return "white"


# create a set of all tasting notes from the data obtained from Vivino
with open("vivino_data_combined.json", mode="r", encoding="utf-8") as json_file:
    wine_data = json.load(json_file)
    
all_tastes = set()

for k in wine_data:
    all_tastes.update(k["wine_tastes"])
    
print(all_tastes)


# writing the data in json file for tastes
data_file = open('all_tastes.json',mode="w", encoding="utf-8" )
jsonString = json.dumps(list(all_tastes))

data_file.write(jsonString)
data_file.close()


## read generated taste file from above
with open("all_tastes.json", mode="r", encoding="utf-8") as json_file:
    all_tastes = json.load(json_file)    
all_tastes.sort()
all_tastes.append("Other") #append other to handle unidentified tastes 

   
## Adding the numerical data for falvors and labesls for wine types in wine dataframe 
df = pd.DataFrame(wine_data)
df["features"] = df.apply(one_hot_encoding, axis = 1)
df["label"] = df.apply(label_encoding, axis = 1)
print(df)


## Use regression function to fit the model and predict missing values for wine types
clf = LogisticRegression(random_state = 0, max_iter = 1000)
clf.fit(df[~df["label"].isna()]["features"].to_list(), df[~df["label"].isna()]["label"].to_list())


df["label"] = df.apply(get_prediction, axis = 1)
df["wine_type_imputed"] = df.apply(label_decoding, axis = 1)

print (df[["wine_id", "wine_name", "wine_type","wine_type_imputed"]])
df1 = df[["wine_id", "wine_name","wine_type_imputed","wine_year","wine_alcohol","wine_country","wine_price"]]
 
    
## writing the data in json file 
data_file = open('imputed_wine_data.json', mode="w", encoding="utf-8" )
jsonString = df1.to_json(orient = 'records')
data_file.write(jsonString)
data_file.close()


