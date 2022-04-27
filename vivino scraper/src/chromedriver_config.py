from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import config
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_chromedriver(webdriver_module=webdriver):

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    userAgent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Mobile Safari/537.36"
    chrome_options.add_argument("user-agent=" + userAgent)

    if(webdriver_module != webdriver):
        chrome_options.add_argument("--proxy-server=localhost:8899")

    chrome_options.headless = config.headless_chrome
    chrome_prefs = {}
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_options.add_argument('lang=en')
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    driver = webdriver_module.Chrome(options=chrome_options,
                                     executable_path=config.chromedriver_path,
                                     desired_capabilities=desired_capabilities)

    driver.set_window_size(1920, 1080)
    return driver
