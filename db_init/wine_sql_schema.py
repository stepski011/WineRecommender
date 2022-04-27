"""
Script for inserting data in PostgreSQL schema by use of sqlalchemy library.
FOr JSON files: Values are inserted in dataframes and added to tables in database.
For CSV files: Values are directly inserted in database.

"""

import pandas as pd
from sqlalchemy import create_engine
import json
from sqlalchemy.types import Integer, Text, String, DateTime, Float, JSON

# Read the data file for Vivino dataset
with open('vivino_data_final.json', mode="r", encoding="utf-8") as dataFile:
    wineDataJSON = json.load(dataFile)

# Create connection with the PostgreSQL db
engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/wines_db")


# Initilaize variables and data structures for inserting tables in database
# Dataframes --> Tables
# Lists --> Columns


# wine
wineTableName = 'wine'
wineDataFrame = pd.DataFrame()
wineNames, wineIds, wineAlcohols, wineTypes, wineYears, wineCountries, wineRegions, winePrices, wineRatings, wineThumbnail = [
], [], [], [], [], [], [], [], [], []

# wineStruct
wineStructTableName = 'wine_structure'
wineStructDataFrame = pd.DataFrame()
wineStructIds, wineAcidity, wineFizziness, wineIntensity, wineSweetness, wineTannin = [
], [], [], [], [], []

# wineFlavor AKA wineTaste
wineFlavorTableName = 'wine_flavor'
wineFlavorDataFrame = pd.DataFrame()
blackFruits, citrusFruit, driedFruit, earth, floral, microbio, nonOak, oak, redFruit, spices, treeFruits, tropicalFruit, vegetal, wineFlavorDescriptions = [
], [], [], [], [], [], [], [], [], [], [], [], [], [] 


# Iterate through the values in dataset and assign values of keys to corresponding lists
for index in range(len(wineDataJSON)):

    wineObject = wineDataJSON[index]
    
    wineIds.append(wineObject['wine_id'] if type(
        wineObject['wine_id']) == int else 0)
    wineNames.append(wineObject['wine_name'] + ' ' + wineObject['wine_winery'])
    wineAlcohols.append(wineObject['wine_alcohol'])
    wineTypes.append(wineObject['wine_type'])
    wineYears.append(wineObject['wine_year'] if type(
        wineObject['wine_year']) == int else 0)
    wineCountries.append(wineObject['wine_country'])
    wineRegions.append(wineObject['wine_region'])
    winePrices.append(wineObject['wine_price'] if type(
        wineObject['wine_price']) == float else 0.00)
    wineRatings.append(wineObject['wine_rating'] if type(
        wineObject['wine_rating']) == float else 0.00)
    wineThumbnail.append(wineObject['wine_thumb'])


    wineStructObject = wineObject['wine_structure']
    if wineStructObject:
        wineAcidity.append(wineStructObject['acidity'] if type(
            wineStructObject['acidity']) == float else 0.00)
        wineFizziness.append(wineStructObject['fizziness'] if type(
            wineStructObject['fizziness']) == float else 0.00)
        wineIntensity.append(wineStructObject['intensity']if type(
            wineStructObject['intensity']) == float else 0.00)
        wineTannin.append(wineStructObject['tannin']if type(
            wineStructObject['tannin']) == float else 0.00)
        wineSweetness.append(wineStructObject['sweetness']if type(
            wineStructObject['sweetness']) == float else 0.00)
        wineStructIds.append(index)

    else:
        wineAcidity.append(0.00)
        wineFizziness.append(0.00)
        wineIntensity.append(0.00)
        wineTannin.append(0.00)
        wineSweetness.append(0.00)
        wineStructIds.append(index)


# Each flavor group  is added as a column with flavour count as value for each wine
    wineTastes = wineObject['wine_tastes']
    if wineTastes is not None:
        for key, value in wineTastes.items():

            if key == 'black_fruit':
                blackFruits.append(value)
            elif key == 'citrus_fruit':
                citrusFruit.append(value)
            elif key == 'dried_fruit':
                driedFruit.append(value)
            elif key == 'earth':
                earth.append(value)
            elif key == 'floral':
                floral.append(value)
            elif key == 'microbio':
                microbio.append(value)
            elif key == 'non_oak':
                nonOak.append(value)
            elif key == 'oak':
                oak.append(value)
            elif key == 'red_fruit':
                redFruit.append(value)
            elif key == 'spices':
                spices.append(value)
            elif key == 'tree_fruit':
                treeFruits.append(value)
            elif key == 'tropical_fruit':
                tropicalFruit.append(value)
            elif key == 'vegetal':
                vegetal.append(value)

# Insert values from lists to corresponding dataframes 

# wine
wineDataFrame.insert(0, 'wine_id', wineIds, False)  # PK of wine table
wineDataFrame.insert(1, 'wine_name', wineNames, False)
wineDataFrame.insert(2, 'wine_alcohol', wineAlcohols, False)
wineDataFrame.insert(3, 'wine_type', wineTypes, False)
wineDataFrame.insert(4, 'wine_year', wineYears, False)
wineDataFrame.insert(5, 'wine_country', wineCountries, False)
wineDataFrame.insert(6, 'wine_region', wineRegions, False)
wineDataFrame.insert(7, 'wine_price', winePrices, False)
wineDataFrame.insert(8, 'wine_rating', wineRatings, False)
wineDataFrame.insert(9, 'wine_thumb', wineThumbnail, False)

# wineStruct
wineStructDataFrame.insert(0, 'wine_structure_id', wineStructIds)  # PK of wine_structure table
wineStructDataFrame.insert(1, 'wine_acidity', wineAcidity)
wineStructDataFrame.insert(2, 'wine_fizziness', wineFizziness)
wineStructDataFrame.insert(3, 'wine_intensity', wineIntensity)
wineStructDataFrame.insert(4, 'wine_tennin', wineIntensity)
wineStructDataFrame.insert(5, 'wine_sweetness', wineSweetness)
wineStructDataFrame.insert(6, 'wine_id', wineIds, False)    # set as FK in database


# wineFlavor
wineFlavorDataFrame.insert(
    0, 'wine_flavor_id', range(1, 1 + len(wineIds)))        # PK of wine_flavor table
wineFlavorDataFrame.insert(1, 'black_fruit', blackFruits)
wineFlavorDataFrame.insert(2, 'citrus_fruit', citrusFruit)
wineFlavorDataFrame.insert(3, 'dried_fruit', driedFruit)
wineFlavorDataFrame.insert(4, 'earth', earth)
wineFlavorDataFrame.insert(5, 'floral', floral)
wineFlavorDataFrame.insert(6, 'microbio', microbio)
wineFlavorDataFrame.insert(7, 'non_oak', nonOak)
wineFlavorDataFrame.insert(8, 'oak', oak)
wineFlavorDataFrame.insert(9, 'red_fruit', redFruit)
wineFlavorDataFrame.insert(10, 'spices', spices)
wineFlavorDataFrame.insert(11, 'tree_fruit', treeFruits)
wineFlavorDataFrame.insert(12, 'tropical_fruit', tropicalFruit)
wineFlavorDataFrame.insert(13, 'vegetal', vegetal)
wineFlavorDataFrame.insert(14, 'wine_id', wineIds, False)   # set as FK in database


# Remove duplicate values 
wineDataFrame.drop_duplicates(subset ="wine_id",keep="first", inplace = True)
wineStructDataFrame.drop_duplicates(subset ="wine_id",keep="first", inplace = True)
wineFlavorDataFrame.drop_duplicates(subset ="wine_id",keep="first", inplace = True)


# Insert dataframes into tables in PostgreSQL
wineDataFrame.to_sql(
    wineTableName,
    engine,
    if_exists='replace', # drop table if already exists
    index=False,
    chunksize=500,
    dtype={
        'wine_id': Integer,
        'wine_name': Text,
        'wine_winery': Text,
        'wine_alcohol': Text,
        'wine_type': Text,
        'wine_year': Integer,
        'wine_country': Text,
        'wine_region': Text,
        'wine_price': Float,
        'wine_rating': Float,
        'wine_thumb': Text
    }
)
wineStructDataFrame.to_sql(
    wineStructTableName,
    engine,
    if_exists='replace',  # drop table if already exists
    index=False,
    chunksize=500,
    dtype={
        'wine_structure_id': Integer,
        'wine_acidity': Float,
        'wine_fizziness': Float,
        'wine_intensity': Float,
        'wine_tannin': Float,
        'wine_sweetness': Float,
        "wine_id": Integer,

    }
)

wineFlavorDataFrame.to_sql(
    wineFlavorTableName,
    engine,
    if_exists='replace', # drop table if already exists
    index=False,
    chunksize=500,
    dtype={
        'wine_flavor_id': Integer,
        'black_fruit': Float,
        'citrus_fruit': Float,
        'dried_fruit': Float,
        'earth': Float,
        'floral': Float,
        'microbio': Float,
        'non_oak': Float,
        'oak': Float,
        'red_fruit': Float,
        'spices': Float,
        'tree_fruit': Float,
        'tropical_fruit': Float,
        'vegetal': Float,
        'wine_id': Integer,

    }
)


# Read the data file for local_wines dataset
df = pd.read_csv('local_wines.csv')
table_name = 'local_wine'
df.columns = [c.lower() for c in df.columns]

# Insert dataframe into local_wine table in PostgreSQL
df.to_sql(
    table_name,
    engine,
    if_exists='replace',
    index=False,
    chunksize=500,
    dtype={
        "lw_id": Integer,       # PK of local_wine table
        "lw_name": Text,
        "lw_country": Text,
        "lw_region": Text,
        "lw_year": Integer,
        "lw_type": Text,
        "lw_price":  Float,
        "lw_url":  Text,
        "lw_thumb": Text,
        "lw_description": Text,
        "lw_seller": Integer,
        "wine_id":Integer       # set as FK in database
    }
)



