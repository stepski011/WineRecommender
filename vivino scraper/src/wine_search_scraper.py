import pathlib

import traceback
import time
import pandas as pd
import json
import os
import chromedriver_config
from vivino_pages import wine_search_page
from config import wine_search_config
filePath = pathlib.Path(__file__).parent.resolve()


driver = chromedriver_config.get_chromedriver()

df = pd.DataFrame(columns=["datetime", "link", "local_id"])

# resume where the previous scrape left of
if os.path.isfile(str(filePath) + "/../temp/product_detail_links/"+wine_search_config.output_filename):
    df = pd.read_csv(
        str(filePath) + "/../temp/product_detail_links/"+wine_search_config.output_filename, index_col=False)

with open(str(filePath)+"/params/wine_search.json", "r") as file:
    json_file = json.load(file)
    i = 0
    n_len = len(json_file)
    for line in json_file:
        i += 1
        print(i, "/", n_len)

        try:

            nId = int(line["local_id"])
            dfId = df.local_id

            # check if local wine id was already scraped
            if(not dfId.isin([nId]).any()):

                wine_search_page.load_search_page(
                    line["search_string"], driver)

                # wait for search results
                search_list = wine_search_page.wait_for_search_results(driver)

                links = wine_search_page.extract_links_from_search_list(
                    search_list)

                # only extract 3 links that lead to a wine detail page
                links = [link for link in links if "/wines/" in link][:3]

                for link in links:
                    df = df.append({"datetime": time.time(),
                                    "link":  link, "local_id": line["local_id"]}, ignore_index=True)
                time.sleep(5)

        except Exception as err:
            print("Fehlermeldung:")
            print(err)
            traceback.print_exc()

# vivino sometimes sends duplicates
df.drop_duplicates("link")
df.to_csv(str(filePath) + "/../temp/product_detail_links/" +
          wine_search_config.output_filename, index_label="scrape_id")
print("file saved")
driver.close()
