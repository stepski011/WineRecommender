# from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from seleniumwire import webdriver as seleniumwire_webdriver
from seleniumwire.utils import decode
import re
import pandas as pd
import bs4

import time
import json

import params.config as config
import pathlib
import datetime
import chromedriver_config


def wait_for_wine_data(driver):
    '''
    This function is used to wait for the wine data to be loaded. This does not include taste data.
    params: driver - selenium webdriver
    '''
    WebDriverWait(driver, config.timeout).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "vintage"))
    )


def wait_for_taste_data(driver):
    '''
    This function is used to wait for the taste data to be loaded. This does not include wine data.
    params: driver - selenium webdriver
    '''
    WebDriverWait(driver, config.loadTime).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'tasteCharacteristics')] "))
    )


def look_for_taste_data(driver, n=5):
    '''
    This function is used to look for taste data on the page. The website scrolls down n times until the taste data is found.
    params: driver - selenium webdriver
    '''
    counter = 0
    while (counter < n):
        try:
            wait_for_taste_data(driver)

            break
        except:
            counter2 = 0
            while counter2 < 10:
                try:

                    driver.execute_script("""window.scrollBy(0,400)""")
                    break
                except:
                    print("error while scrolling")
                    time.sleep(1)
                    counter2 += 1
        counter += 1


def get_wine_data(driver):
    '''
    This function is used to extract wine data from the opened page.
    params: driver - selenium webdriver
    return: python dict with all taste data available
    '''

    soup = bs4.BeautifulSoup(driver.page_source, features="html.parser")
    for elem in soup.findAll("script"):
        script = str(elem)
        if '{"vintage":' in script:

            line = script.splitlines()[3]

            if line[-1] == ";":
                line = line[:-1]

            jsonString = line[line.index('{"vintage"'):]
            return json.loads(jsonString)
