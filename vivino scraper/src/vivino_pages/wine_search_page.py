

import pathlib
from signal import SIG_DFL
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

import traceback


from bs4 import BeautifulSoup
import time
import params.config as config
import pandas as pd
import json
import os
import chromedriver_config


def load_search_page(search_string, driver):
    '''
    This function is used to open the search results for a search string.
    params:
        search_string - string that should be searched 
        driver - selenium webdriver
    '''
    driver.get("https://www.vivino.com/search/wines?q=" +
               str(search_string))


def wait_for_search_results(driver):
    '''
    This function is used to for the results of a search to be loaded .
    params: driver - selenium webdriver
    return: webdriver element for search list
    '''
    return WebDriverWait(driver, config.timeout).until(
        EC.presence_of_element_located(
                        (By.XPATH, '//div[@class="search-results-list"]'))
    )


def extract_links_from_search_list(search_list):
    '''
    This function is used to extract all links from a search lists.
    params: search_list - webelement for search list
    return: all links in the search list
    '''
    html = search_list.get_attribute('innerHTML')
    attributes = BeautifulSoup(
        html, 'html.parser').find_all('a', href=True)

    return [attr["href"] for attr in attributes]
