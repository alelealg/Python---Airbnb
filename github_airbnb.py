newyork = "https://www.airbnb.com/s/Manhattan--New-York-City--New-York--Verenigde-Staten/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&place_id=ChIJYeZuBI9YwokRjMDs_IEyCwo&source=structured_search_input_header&search_type=search_query&query=Manhattan%2C%20New%20York%20City%2C%20New%20York&checkin=2020-08-01&checkout=2020-08-08&adults=1&locale=en&_set_bev_on_new_domain=1592849383_ZmI4NzE3ZDMyMWU4"
tokyo = "https://www.airbnb.com/s/Tokyo--Japan/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&place_id=ChIJ51cu8IcbXWARiRtXIothAS4&source=structured_search_input_header&search_type=search_query&query=Tokyo%2C%20Japan&checkin=2020-08-01&checkout=2020-08-08&adults=1&_set_bev_on_new_domain=1592849383_ZmI4NzE3ZDMyMWU4&locale=en#simple-header-locale-menu"
tzintzuntzan = 'https://www.airbnb.mx/s/Tzintzuntzan/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=autocomplete_click&query=Tzintzuntzan&place_id=ChIJUcqmhhu9LYQRZZLknhAcQSs'
"""
    Setting up your environment
"""
from bs4 import BeautifulSoup
from selenium import webdriver
# The following packages will also be used in this tutorial
import pandas as pd
import numpy as np
import time
import requests
import re
from sklearn.feature_extraction.text import CountVectorizer
from joblib import Parallel, delayed

"""
    Getting started
"""


def getPage(url):
    ''' returns a soup object that contains all the information
    of a certain webpage'''
    result = requests.get(url)
    content = result.content
    return BeautifulSoup(content, features="lxml")


def getRoomClasses(soupPage):
    ''' This function returns all the listings that can
    be found on the page in a list.'''
    rooms = soupPage.findAll("div", {"class": "_8ssblpx"})
    result = []
    for room in rooms:
        result.append(room)
    return result


def getListingTitle(listing):
    ''' This function returns the title of the listing'''
    return listing.find("meta")["content"]


def getTopRow(listing):
    ''' Returns the top row of listing information'''
    return listing.find("div", {"class": "_167qordg"}).text


def getRoomInfo(listing):
    ''' Returns the guest information'''
    return listing.find("div", {"class": "_kqh46o"}).text


def getBasicFacilities(listing):
    ''' Returns the basic facilities'''
    try:
        output = listing.findAll("div", {"class": "_kqh46o"})[1].text.replace(" ", "")  # Speeds up cleaning
    except:
        output = []
    return output


def getListingPrice(listing):
    ''' Returns the price'''
    return listing.find("div", {"class": "_1fwiw8gv"}).text


def getListingRating(listing):
    ''' Returns the rating '''
    return listing.find("span", {"class": "_krjbj"}).text


def getListingReviewNumber(listing):
    ''' Returns the number of reviews '''
    try:  # Not all listings have reviews // extraction failed
        output = listing.findAll("span", {"class": "_krjbj"})[1].text
    except:
        output = -1  # Indicate that the extraction failed -> can indicate no reviews or a mistake in scraping
    return output


def extractInformation(soupPage):
    ''' Takes all the information of a single page (thus multiple listings) and
    summarizes it in a dataframe'''
    listings = getRoomClasses(soupPage)
    titles, links, toprows, roominfos, basicfacilitiess, prices, ratings, reviews = [], [], [], [], [], [], [], []
    for listing in listings:
        titles.append(getListingTitle(listing))
        toprows.append(getTopRow(listing))
        roominfos.append(getRoomInfo(listing))
        basicfacilitiess.append(getBasicFacilities(listing))
        prices.append(getListingPrice(listing))
        ratings.append(getListingRating(listing))
        reviews.append(getListingReviewNumber(listing))
    dictionary = {"title": titles, "toprow": toprows, "roominfo": roominfos, "facilities": basicfacilitiess,
                  "price": prices, "rating": ratings, "reviewnumber": reviews}
    return pd.DataFrame(dictionary)


'''
    Scraping all listings for a given city
'''


def findNextPage(soupPage):
    ''' Finds the next page with listings if it exists '''
    try:
        nextpage = "https://airbnb.com" + soupPage.find("li", {"class": "_i66xk8d"}).find("a")["href"]
    except:
        nextpage = "no next page"
    return nextpage


def getPages(url):
    ''' This function returns all the links to the pages containing
    listings for one particular city '''
    result = []
    while url != "no next page":
        page = getPage(url)
        result = result + [page]
        url = findNextPage(page)
    return result


def extractPages(url):
    ''' This function outputs a dataframe that contains all information of a particular
    city. It thus contains information of multiple listings coming from multiple pages.'''
    pages = getPages(url)
    # Do for the first element to initialize the dataframe
    df = extractInformation(pages[0])
    # Loop over all other elements of the dataframe
    for pagenumber in range(1, len(pages)):
        df = df.append(extractInformation(pages[pagenumber]))
    return df


''' 
    Scraping all listings for a collection of cities
'''

url = 'https://www.airbnb.mx/s/Tzintzuntzan/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=autocomplete_click&query=Tzintzuntzan&place_id=ChIJUcqmhhu9LYQRZZLknhAcQSs'

'''
    Scraper
'''


def scraper(url, sample_size=None, random_state=1234):
    df = extractPages(url)
    return df

df1 = scraper(url, sample_size = 100)



print(df1.head())

print(df1[['reviewnumber']])
