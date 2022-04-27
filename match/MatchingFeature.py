#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stepski
"""

# record linkage version 1

import numpy as np
import pandas as pd
#import pip
#pip.main(["install", "recordlinkage"])
import recordlinkage
#import pip
#pip.main(["install", "fuzzywuzzy"])
from fuzzywuzzy import fuzz


vivino = pd.read_csv("vivino.csv")
local = pd.read_csv("local.csv")

vivino = vivino[["id", "wine_name", "wine_year", "wine_type", "wine_price", "wine_alcohol", "wine_tastes"]]
local = local[["id", "wine_name", "wine_year", "wine_type", "wine_price", "wine_alcohol", "wine_region", "wine_seller"]]


class RecordsMatching():    

    indexer = recordlinkage.Index()
    indexer.block('wine_type')
    candidate_links = indexer.index(vivino, local)

    c = recordlinkage.Compare()

    c.string('wine_name', 'wine_name', method='jarowinkler', threshold=0.47)
    # Error in next numeric comparsion
    
    # TypeError: unsupported operand type(s) for -: 'object' and 'float64'
    c.numeric('wine_alcohol', 'wine_alcohol', missing_value=0.5)
    c.numeric("wine_price", "wine_price", missing_value=0.5)
    
    feature_vectors = c.compute(candidate_links, vivino, local)
    
    #Expectation-Conditional Maximisation    
    def ECM():
        ecm = recordlinkage.ECMClassifier()
        compare = feature_vectors=feature_vectors[[col for col in feature_vectors.columns if feature_vectors[col].nunique() >= 2]]

class BruteForceMatch():
    
    # O(n1*n2) = 12mil iterations = up to 10 minutes
    def MatchingName(list1,list2):
        no_matching = []
        matching = []
        m_score = 0
        for item1 in vivino["wine_name"]:
            for item2 in local["wine_name"]:
                m_score = fuzz.ratio(item1, item2)
                # Optimization of threshold value - setted up to 47
                if m_score > 47:
                    matching.append(item1)
            if m_score < 47 and not(item1 in matching):
                no_matching.append(item1)
        return(no_matching)
            
    file = open("no_matches.txt", "w")
    for element in no_matching_wines:
        file.write(element + "\n")
    file.close()
    
    
    
# Rapid fuzz

from rapidfuzz import process, fuzz

scores = process.cdist(
    vivino["wine_name"], local["wine_name"], scorer=fuzz.ratio,
    dtype=np.uint8, score_cutoff=55)

matches = np.any(scores, 1)

matching = [x for x, is_match in zip(vivino["wine_name"], matches) if is_match]
not_matching = [x for x, is_match in zip(vivino["wine_name"], matches) if not is_match]

