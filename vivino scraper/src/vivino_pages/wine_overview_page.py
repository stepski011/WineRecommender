import pathlib
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


def wait_for_winecard(driver):
    '''
    This function is used to wait for at least one winecard to be present. A winecard is the widget that is used to show one search result.
    params: driver - selenium webdriver
    return: webdriver element for winecard
    '''
    element = WebDriverWait(driver, config.timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@id='explore-page-app']/div/div/div[2]/div[2]/div[1]/div[1]"))
    )
    return element


def get_links_from_winecard(winecard):
    '''
    This function is used to extract links from a winecard.
    params: winecard - webdriver element for winecard
    return: all links for the winecard
    '''
    html = winecard.get_attribute('outerHTML')
    return BeautifulSoup(html, 'html.parser').a.attrs["href"]


def remove_first_winecard(driver):
    '''
    This function is used to remove the first winecard on a page.
    params: driver - selenium webdriver
    '''
    driver.execute_script("""
            var results = document.getElementsByClassName("explorerPage__results--3wqLw")[0]
            results.children[0].removeChild(results.children[0].firstChild)
            """)
