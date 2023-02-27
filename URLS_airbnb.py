import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def sopa(url):
    sopa = requests.get(url).content
    return BeautifulSoup(sopa, features="lxml")

def pag_sig(pagsopa):
    ''' Finds the next page with listings if it exists '''
    try:
        pagsig = "https://airbnb.com" + pagsopa.find("li", {"class": "_i66xk8d"}).find("a")["href"]
    except:
        pagsig = "no next page"
    return pagsig


def getPages(url):
    ''' This function returns all the links to the pages containing
    listings for one particular city '''
    result = []
    while url != "no next page":
        page = sopa(url)
        result = result + [page]
        url = pag_sig(page)
    return result

pages = getPages('https://www.airbnb.mx/s/Tzintzuntzan/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=autocomplete_click&query=Tzintzuntzan&place_id=ChIJUcqmhhu9LYQRZZLknhAcQSs')
print(pages)