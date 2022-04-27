#! /usr/bin/env python3
import sys
import os
import json
import csv
import pandas
from pathlib import Path
 

 

def wineType(id):
    switch = {
        1: 'red',
        2: 'white',
        3: 'sparkling',
        4: 'rosé'
    }

    return switch.get(id, 'sparkling')

def normalizeTaste(val, max_mentions):
    if val is None:
        val = 0
    else: 
        val = val/max_mentions
    return val

def get_wine_profile(data, keys):
    out = {}

    # get highest mention count
    max_mentions = max(data.values())
    
    # compute normalized mention count
    for key in keys:
        try:
            out[key] = normalizeTaste(data[key], max_mentions)
        except:
            out[key] = 0

    
    return out

def normalizeStructure(wine_structure):
    keys = ["acidity", "fizziness", "intensity", "sweetness", "tannin"]
    normalized = {}
    for key in keys:
        if wine_structure[key] is None:
            normalized[key] = 0
        else:
            normalized[key] = (wine_structure[key] - 1)/4
    return normalized

taste_path = []
vintage_path = []
dictList = []
myList = []
price = 0
rose = 0
red = 0
white = 0
sparkling = 0
others = 0
wine_name = "none"
#define fixed list of taste group keys
keys = ['black_fruit', 'citrus_fruit', 'dried_fruit', 'earth', 'floral', 'microbio', 'non_oak', 'oak', 'red_fruit', 'spices', 'tree_fruit', 'tropical_fruit', 'vegetal']
# get working directory and iterate over folders to generate dataset
path = os.getcwd()
wineDirs = os.listdir(path)

#only required because the folder structure is data/export {1,2}/...
wineFolders = []
for wineDir in wineDirs:
    wineFolders.extend([wineDir+'/'+x for x in os.listdir(wineDir)])

for wineFolder in wineFolders:
    try:        
        # Opening JSON file and loading the data into the variable data

        with open('/'.join([path, wineFolder,'vintage.json']), mode="r", encoding="utf-8") as json_file:
            wine_data = json.load(json_file)
        try:    
            with open('/'.join([path, wineFolder,'taste.json']), mode="r", encoding="utf-8") as json_file:
                taste_data = json.load(json_file)
        except:
            taste_data = None   
        
        # Extracting desired attributes from vintage.json 
        vintage = wine_data["vintage"]
        wine = wine_data["vintage"]["wine"]
        wine_id = wine["id"]
        wine_name = wine["name"]
        wine_facts = vintage["wine_facts"]
        wine_winery = wine["winery"]["name"]
        wine_rating = vintage["statistics"]["ratings_average"]
        if "alcohol" in wine_facts.keys():
            wine_alcohol = wine_facts['alcohol']
        else: 
            wine_alcohol = 0
        wine_year = vintage['year']
        region = wine['region']
        if region != None:
            wine_region = region['name']
            wine_country = region['country']['name']
        
            
        # Extracting price from vintage.json 
        if 'price' in wine_data.keys():
            price_key = wine_data['price']
            if price_key != None:
                wine_price = price_key['amount']
                print("Count: " + str(price))
                price += 1
        else:
            wine_price = 0


        wine_type = wineType(wine['type_id']) 
        wine_thumb = vintage["image"]["location"]    
        
        # Extracting desired attributes from taste.json 
        
        try:
            taste = taste_data["tastes"]
            flavor = taste["flavor"]
            wine_structure = taste["structure"]
            wine_tastes = {}
            for g in flavor:
                wine_tastes[g["group"]] = g["stats"]["mentions_count"]
                
            try:
                wine_tastes = get_wine_profile(wine_tastes, keys)        
            except Exception as e:
                print("no taste data")
                continue
            
            try:
                
                wine_structure = normalizeStructure(wine_structure)
            except Exception as e:
                print('Errored during structure normalization with: '+e)
        except:
            print('no flavor data present')
            continue

        


        
        wine_dict = {
            "wine_id" : wine_id,
            "wine_name" : wine_name,
            "wine_winery" : wine_winery,
            "wine_alcohol" : wine_alcohol,
            "wine_type" : wine_type,
            "wine_year" : wine_year,
            "wine_country" : wine_country,
            "wine_region": wine_region,
            "wine_price" : wine_price,
            "wine_structure": wine_structure,
            "wine_tastes": wine_tastes,
            "wine_rating" : wine_rating,
            "wine_thumb" : wine_thumb
            
        }
        dictList.append(wine_dict)

    except Exception as e: {
        print(e) }

        

# writing the data in json file 
data_file = open('vivino_data.json',mode="w", encoding="utf-8" )
jsonString = json.dumps(dictList)

data_file.write(jsonString)

data_file.close()

print ("WHITE count: " + str(white))
print ('RED count: ' + str(red))
print ("ROSE count: " + str(rose))
print ("Sparkling count: " + str(sparkling))
print ("Others count: " + str(others))


