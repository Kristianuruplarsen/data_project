
import pandas as pd 
import numpy as np 
import string 

def letterDensity(authors):
    """ Calculate the empirical distribution of first letters.
    """
    authors['firstLetter'] = authors.firstLetter.apply(lambda x: x.lower())
    authors = authors[authors['firstLetter'].isin([i for i in string.ascii_lowercase])]
    byLetter = authors.groupby('firstLetter').name.agg('count')
    total = byLetter.sum()

    return byLetter / total


def before(all_auths):
    """ Check if `our` author will be first author in the 
    set of `all_` authors.
    """
    d = {k:0 for k in all_auths}
    d[sorted(all_auths)[0]] = 1  # This was the first author
    
    return d


def simulate_paper(authors, n_authors, p_letter, alphabet):
    """ Simulate a single paper.
    1) Draw `n_authors` random letters from the alphabet 
       with replacement. These represent the authors of 
       the paper. 
       
    2) Randomly select one of these to be "our" author.
    3) Check if our author is alphabetically first author, 
       or not. Then return this as a 1/0 variable, as well
       as the letter of "our" author.
    """
    
    # Simulate all authors
    all_authors = np.random.choice(alphabet, p=p_letter, size= n_authors, replace=True)
        
    return before(all_authors)


def simulate(authors, n_authors = 3, rounds = 100):
    """ Simulate a bunch of papers, to get a 
    distribution over all letters in the alph-
    abet
    """
    data = {k:list() for k in string.ascii_lowercase}
    p_letter = letterDensity(authors)
    alphab = [i for i in string.ascii_lowercase]
    
    for _ in range(rounds):
        paper_data = simulate_paper(authors, n_authors, p_letter, alphab)
        
        for alph in paper_data.keys():
            data[alph].append(paper_data[alph])
    
    return data
        