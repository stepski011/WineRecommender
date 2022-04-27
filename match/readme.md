# Readme

## Functionality 
This folder contains all parts required for data processing and data matching.

## Requirements 
- Python 3.x (In testing 3.9.2 was used)
- all necessary pip packages:
    use pip install -r requirements

## Contents
The data_matching notebook contains all relevant code used for our minimum viable product.
Please note that the notebook contains some commented out cells. These were used either in early testing and/or initial matching, but no longer required to achieve the full set of results. Nevertheless, they were kept for posterity.

The contained .csv files are the output of this process.
fuzzy_results_all.csv is the output the fuzzymatcher package produces.
local_wines_matched.csv is the list of local wines with the corresponding Vivino wine id added.

initial_fuzz: contains the results of our first testing round of fuzzy matching, resulting in the lists of wines to be rescraped from vivino in the rescrape subdirectory.


intermediate_results: contains intermediate results of the data processing steps that are kept for testing and/or as backup.

other_attempts: contains all files related to other attempts at data matching.