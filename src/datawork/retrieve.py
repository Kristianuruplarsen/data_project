
"""
Functions for downloading data from Ideas.
"""

import requests 
import pandas as pd 
import os 
from bs4 import BeautifulSoup

from .utils import * 



def cached(func, path, *scraper_args):
    """ Add caching to a scraper. 
    """
    if not os.path.exists(path):
        data = func(*scraper_args)
        data.to_csv(path, index = False)
        print("Scraped from web.")
    else:
        data = pd.read_csv(path)
        print("Read from file.")
    return data



def get_authors(nskip = 10):
    """ Get basic information for each author in the Ideas database. 

    Params 
    ------
        nskip(int, optional): how many bs4 results to skip. 

    Returns 
    -------
        pandas.DataFrame
    """
    url = 'https://ideas.repec.org/i/eall.html'
    resp = requests.get(url)

    if not resp.ok:
        raise ValueError("Response is bad")

    soup = BeautifulSoup(resp.text, 'lxml')
    authors = soup.findAll('td')[nskip:]

    # extract data
    links = [findLink(auth) for auth in authors]
    names = [findName(auth) for auth in authors]
    pubcount= [findPubs(auth) for auth in authors]

    return pd.DataFrame({'name': names, 'url': links, 'pubs': pubcount})




def get_author_work(url):
    """ Get the complete list of work by an author.

    Params 
    ------
        url(str): The Ideas url of the author.

    Returns
    -------
        pd.DataFrame
    """
    url = f'https://ideas.repec.org{url}'
    resp = requests.get(url)
    assert resp.ok, f"Request failed when getting {url}"

    soup = BeautifulSoup(resp.text, 'lxml')
    allwork = soup.find_all('li', class_='list-group-item')

    def getLink(w):
        try:
            return w.a['href']
        except:
            return None

    def getAuthor(w):
        try:
            return w.getText().split('\n')[0]
        except:
            return None

    def getYear(w):
        try:
            return w.getText().split('\n')[0].split(',')[-1]
        except:
            return None

    def getTitle(w):
        try:
            return w.a.getText()
        except:
            return None

    def getJournal(w):
        try:
            return w.find_all('a')[1]['href'], w.find_all('a')[1].getText()
        except:
            return None

    def getJournalLink(j):
        try:
            return j[0]
        except:
            return None

    def getJournalName(j):
        try:
            return j[1]
        except:
            return None

    links = [getLink(w) for w in allwork]
    authors = [getAuthor(w) for w in allwork]
    year = [getYear(w) for w in allwork]
    title = [getTitle(w) for w in allwork]
    jrnl =  [getJournal(w) for w in allwork]
    journal = [getJournalLink(j) for j in jrnl]
    journalName = [getJournalName(j) for j in jrnl]

    data = pd.DataFrame( {'url': links, 'authors': authors,
                        'year': year, 'title': title,
                        'journal_url': journal,
                        'journal_name': journalName} )

    return data
     