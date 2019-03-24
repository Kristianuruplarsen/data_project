
""" 
Functions for aggregating and manipulating 
the Ideas dataset.
"""

import re 
import pandas as pd 
import numpy as np 


def build(x):
    """ Build variables from information in the author files.  q
    """

    name = ''.join(re.findall('[A-Za-z]+', x['name']))

    try:
        author_data = pd.read_csv(f'data/authorsWork/{name}.csv')
        
    except:
        x['coauthors'] = list()
        x['unique_journals'] = list()
        x['share_first'] = -1.0
        return x 
    
    x['coauthors'] = _get_coauthors(author_data)
    x['unique_journals'] = _get_journals(author_data)
    x['share_first'] = _get_share_first(author_data, name)

    return x 




def _is_firstauthor(authorstring, name):
    """ Check if `name`is first author in the 
    string of authors for a publication.
    
    Params
    ------
        authorstring(str): all authors of the publication.
        name(str): name of author to check.
    """
    
    firstauthor = authorstring.split('&')[0].strip()
    firstauthor = ''.join(re.findall('[A-Za-z]+', firstauthor))
    
    if sorted(firstauthor.lower()) == sorted(name.lower()):
        return 1 
    return 0 


def _get_share_first(author_data, name):
    """ Get the share of publications the author with 
    name `name` is first author.
    """
    seq = author_data.authors.apply(lambda x: _is_firstauthor(x, name))
    return np.mean(seq)



def _get_all_authors(papers):
    """ Get all coauthors of in a list of papers.
    
    Params
    ------
        papers(iterable): a list of clean coauthor 
            lists.
    
    Returns
    -------
        list
    """
    allauthors = list() 

    for paper in papers:
        for author in paper:
            if author not in allauthors:
                allauthors.append(author)

    return allauthors


def _clean_authors(authorstring):
    """ Convert a string of coauthors into a list 
    with author name sets. 
    
    Params
    ------
        coauthors(str): a raw string of paper authors.
    
    Returns 
    -------
        list
    """
    authorlist = authorstring.split('&')
    
    names = list()
    for author in authorlist:
        
        authorName = ''.join(re.findall('[A-Za-z\s]*', author)).strip().lower()
        anames = set(authorName.split(' '))
        
        names.append(anames)
    
    return names


def _get_coauthors(author_data):
    """ Get all coauthors of an author by name. 
    This function is intended to be used with .apply on a 
    pandas dataframe. 

    Params
    ------
        name(str): name of author

    Returns
    -------
        list
    """
    
    coauthors_raw = author_data.authors.apply(_clean_authors)
    all_coauthors = _get_all_authors(coauthors_raw)
    
    return all_coauthors



def _get_journals(author_data):
    """ Get the journals in which an author has published. 
    
    Params 
    ------
        name(str): name of author
    
    Returns 
    -------
        list
    """
    return list(set(author_data.journal_name))
