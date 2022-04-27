# from selenium import webdriver
import os
from seleniumwire import webdriver as seleniumwire_webdriver
from seleniumwire.utils import decode
import re
import pandas as pd

import time
import json

import config.config as config
import pathlib
import datetime
import chromedriver_config
from vivino_pages import wine_detail_page

driver = chromedriver_config.get_chromedriver(
    webdriver_module=seleniumwire_webdriver)

filePath = pathlib.Path(__file__).parent.resolve()


df = pd.read_csv(str(filePath)+"/../temp/wines_export.csv")

# create export folder
if not os.path.isdir(str(filePath) + "/../export"):
    os.mkdir(str(filePath) + "/../export")

time0 = datetime.datetime.utcnow()
for id, row in df.iterrows():
    print(id, "/", len(df))

    current_wine_dir_path = str(
        filePath) + "/../export/" + str(id) + "/"

    # check if wine was already scraped
    if not(os.path.isfile(current_wine_dir_path+"vintage.json")):

        # create folder
        if not os.path.isdir(current_wine_dir_path):
            os.mkdir(current_wine_dir_path)
            file = open(current_wine_dir_path+"wine_id",
                        "w").write(str(row["local_id"]))

        # interceptor function which checks every call for taste data
        def interceptor(request, response):
            global id
            if(re.match("http[s]?://www\.vivino\.com\/api\/wines\/.*\/tastes.*", request.url)):
                with open(current_wine_dir_path+"taste.json", "w") as taste_file:
                    pattern = re.compile("(?<=/wines\/)\d.*(?=\/tastes)|$")
                    id = re.findall(pattern, request.url)[0]
                    taste_data = json.loads(decode(response.body, response.headers.get(
                        'Content-Encoding', 'identity')))
                    taste_data["vivino_id"] = id
                    json.dump(taste_data, taste_file)

        # set interceptor
        driver.response_interceptor = interceptor
        driver.get("http://www.vivino.com" + row["link"])

        wine_detail_page.wait_for_wine_data(driver)

        # safe wine data
        with open(current_wine_dir_path+"vintage.json", "w") as vintage_file:
            json.dump(wine_detail_page.get_wine_data(driver), vintage_file)

        # check for taste data or scroll down
        wine_detail_page.look_for_taste_data(driver)

        # compute time spend
        time.sleep(config.sleepTime)
        time_now = datetime.datetime.utcnow()
        print("secs per page:", (time_now - time0).total_seconds())
        time0 = time_now
