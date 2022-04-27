import pathlib
import traceback
import time
import config.config as config
import pandas as pd
from vivino_pages import wine_overview_page
import chromedriver_config
from config import wine_overview_config
# setup
filePath = pathlib.Path(__file__).parent.resolve()
driver = chromedriver_config.get_chromedriver()
df = pd.DataFrame()
driver.get(wine_overview_config.link)

try:
    time.sleep(5)
    while True:
        time.sleep(config.sleepTime)

        winecard = wine_overview_page.wait_for_winecard(driver)

        links = wine_overview_page.get_links_from_winecard(winecard)

        df = df.append({"datetime": time.time(),
                        "link":  links}, ignore_index=True)

        # This is done to limit memory usage of chrome
        # After all elements on the page are removed new content is automatically loaded
        wine_overview_page.remove_first_winecard(driver)


except Exception as err:
    # At some point there are no more wines or the API refuses to send more wines
    print("error message:")
    print(err)
    traceback.print_exc()

# vivino sometimes sends duplicates
df.drop_duplicates("link")
df.to_csv(str(filePath) + "/../temp/product_detail_links/" +
          wine_overview_config.link_file_name)
driver.close()
