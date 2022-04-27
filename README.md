<meta charset="UTF-8">
<h1 align="center">Wine MS<p>&#127863;</p> </h1>
<h4 align="center">Wine Recommender system for local wine vendors in Münster town.</h4>

<p align="center">
  <a href="#description">Description</a> •
  <a href="#requirements">Requirements</a> •
  <a href="#modules">Modules</a> •
  <a href="#dir">DIR</a> •
  <a href="#activation">Activation</a> •
  <a href="#authorization">Authorization</a> •
</p>

---

## Description
Wine MS is system consists of large wine database with detail information. The recommendation engine is developed for generating the most similar type according to user taste. Users are supposed to insert their preferences for wine taste and origin, which can be further modified with spider diagram for making more precise taste range. Engine will consider you choice and refer user to the most suitable wine, which you can buy in wine shops all around the Münster (and other towns).

## Requirements

NodeJS & React are required for running the API and User Interface. Check the requirements files in order to start specific module of system.

## Modules

Reference to data scraping, importing to local database and matching retrieved data. 

#### Scraping

The local vine data is retrieved from 3 vendors. Most of scrpaing modules require both libraries: [beaufitfulsoup](https://pypi.org/project/beautifulsoup4/), with any parses, and [Selenium](https://selenium-python.readthedocs.io/) for SSS.

#### Vivino Scraping


##### Functionality

This module is used to scrape vivino data from overview pages of vivino

##### Requirements

In order to use this software following software has to be installed:

- Python 3.x (In testing 3.8 was used)
- all necessary pip packages:
    use pip install -r requirements
- Chrome with ChromeDriver (in testing Chrome 98 was used with ChromeDriver 98.0.4758.102)
    See [ChromeDriver Documentation](https://chromedriver.chromium.org/home) for more information
    The chromedriver file has to be copied to ./dependencies or the path has to be specified in the ./src/config/config.py

##### Usage

1. modify the configs described below.
2. Start scraping. Refer to Config below for more details about configuration.
2.1 run wine_overview_scraper.py. Repeat for all overview pages that you want to scraper
2.2 run wine_search_scraper.py.
3. run combine_links to create a shared wines_export.csv with all links
4. run wine_detail_page_scraper.py to scrape the vintage and taste data.
5. The results are stored in ./export

The easiest way to test this is using the vscode debug configurations.

##### Config

There are three config files which are all located in src/config.

- config.py is used as a general config file and used by all parts of the program
- wine_overview_config.py is used to configure the overview page scraper. This includes link to scrape and output file.
- wine_search_config.py is used to configure the wine search. This includes the output file.
There is also wine_search.json which is used to provide search terms and matched local ids to be scraped.

##### Transforming Scraping Results
We have included our scraping results as vivino_raw.zip.
To transform the scraping results from individual folders to an easily loadable list of item dictionaries, the enclosed extraction.py needs to be run from the command line within the top level vivino_raw folder. Since scraping was done in multiple runs, multiple export folders with identical subfolder names were generated. To combat this, the script was modified accordingly to iterate over all subfolders of the meta-level folder.
The resulting output of the script is included as vivino_data.json.

#### Importing to DB:
```
sqlalchemy
```

#### Matching:
Experimental module for matching wine. For more details refere to documentation. 

```
recordlinkage
fuzzywuzzy
rapidfuzz
```

## DIR

```
api
    WineAPI/                         contains scripts for running the API
    WineRecommedner_API/             contains API configuration scripts

db_init                               contains script for initializing database

ext
                                      contains scripts extracting big amount of data from JSON file & regression imputation of missing values
    
local_scrapers
                                      contains scripts for scraping the data from local vendor's sites
    
match
                                      overlap_matching/     contains experimental scripts for TF-IDF matching
                                      contains scripts for matching wine data
     
ui
    dist/                             contains additional information about wines app
    src/                              contains source coude of React app
    
vivino scraper
    src/                              contains source code for vivino scraper
    
```
## Activation

Install all packages denoted in the requirements.txt file. Modern IDEs should install them automatically. If not use pip (https://pypi.org/project/pip/) to install all the packages from the requirements.txt file. To run the API (assuming you're in the parent \WineRecommender_API>\ folder), run the command:
```
python manage.py runserver
```

## Authorization
All data was retrieved, gathered and processed within the project scope for educational purposes. Main data sources are vivino and Münster wine vendors. The system is developed for Data Integration module at Westfälische Wilhelms Universität, and deployed on local and virtual machines. 
