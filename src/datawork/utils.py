
from bs4 import BeautifulSoup


def removeParenthesis(s):
    """ Remove parentheses from a string.

    Params
    ------
    s (str): String with parenthesis.
    """
    for p in ('(', ')'):
        s = s.replace(p, '')
    return s 


def findLink(author):
    """ Find the link to an author
    """
    try:
        return author.find('a')['href']
    except:
        return ''
    

def findName(author):
    try:
        return author.find('a').getText().strip()
    except:
        return ''
    
    
def findPubs(author):
    try:
        return removeParenthesis( author.find(text = True, recursive = False).strip() )
    except:
        return ''