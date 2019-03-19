
import re 
import pandas as pd 


def get_coauthors(name):
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
    name = ''.join(re.findall('[A-Za-z]+', name))
    try:
        author_data = pd.read_csv(f'data/authorsWork/{name}.csv')
    except:
        return list()

    coauthors_raw = author_data.authors.apply(clean_authors)
    all_coauthors = get_all_authors(coauthors_raw)
    
    return all_coauthors


def get_all_authors(papers):
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


def clean_authors(authorstring):
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
        
        authorName = ''.join(re.findall('[A-Za-z\s]*', author)).strip()
        anames = set(authorName.split(' '))
        
        names.append(anames)
    
    return names

