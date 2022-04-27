from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


def scrape_wines(url, output, headers):
    """
    Scrape wines from https://www.wein-direktimport.de
    :param url: Full URL after choosing desired filters and choosing the number of elements per page e.g. https://www.wein-direktimport.de/alle-weine/land/deutschland/?p=1&o=1&n=96&f=1992
    :param output: Apsolute path where the data will be saved as XLSX file e.g. C:/Users/user/Desktop/wines.xlsx
    :return:
    """

    data = []
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')

    page_to_parent_elem = soup.find('span', {"class": "paging--display"})

    page_to = 1
    if page_to_parent_elem:
        page_to = page_to_parent_elem.find('strong').text

    for i in range(1, int(page_to) + 1):
        if i != 1:
            req = requests.get(url.replace(f'p=1', f'p={i}'))
            soup = BeautifulSoup(req.text, 'lxml')

        wines = soup.find_all('div', {"class": "product--info"})
        for wine in wines:
            price = None
            try:
                price = wine.find('div', attrs={"class": 'product--price'}).find('span').text
                price = re.findall("\d+(?:\.\d+)?,\d+", price)[0]
            except:
                price = None
            url_details = wine.find('a', attrs={"class": 'product--image'})['href']

            imageContainer = wine.find('span', attrs={"class": 'image--media'})

            image = None
            try:
                if imageContainer:
                    image = wine.find('img')['src']
            except:
                if imageContainer:
                    image = wine.find('img')['srcset'].split(',')[0]

            details = requests.get(url_details)
            soup = BeautifulSoup(details.text, 'lxml')
            name = soup.find('h1', attrs={"class": 'product--title'}).text

            tasting_note = ''
            spans = soup.find_all('span', attrs={"class": 'entry--content'})
            for span in spans:
                for tag in span.find_all('p'):
                    tasting_note += f' {tag.text}'

            row_data = {'Name:': name, 'Verkostungsnotiz:': tasting_note, 'Preis:': price, 'Details-URL:': url_details, 'Image:': image}
            details = soup.find('table', attrs={"class": 'product--properties'})
            details_rows = details.find_all('tr')
            for row in details_rows:
                row_details = row.find_all('td')

                header = row_details[0].find('span').text
                row_data[header] = row_details[1].text

            data.append(row_data)

    df = pd.DataFrame(data, columns=headers)
    df.to_excel(output, engine='xlsxwriter')
