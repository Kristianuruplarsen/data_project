
import matplotlib 
import matplotlib.pyplot as plt 
from matplotlib.ticker import FuncFormatter

import pretty 
import seaborn as sns 

import string 

def PublicationsHistogram(data):
    """ Plot figure 1.

    Params
    ------
        data(pd.DataFrame): a suitable dataset
    """
    with pretty.Classic():
        fig = plt.figure(figsize = (12,8))    
        ax = fig.add_subplot(1, 1, 1)
        ax.hist(data.pubs, alpha = 0.4, bins = 60)
        
        ax.grid(which='minor', alpha=0.4, axis='y', linestyle='dotted')
        ax.grid(which='major', alpha=0.8, linestyle='dotted')
        ax.annotate('$\mathbf{FIG.1.}$', xy=(0, 1.015), xycoords='axes fraction', ha='left',
                fontsize=18, annotation_clip=False)
        ax.annotate('$Pulications \ count$', xy=(0.105, 1.015), xycoords='axes fraction', ha='left',
                fontsize=18, annotation_clip=False)
        ax.set_xlabel("Publications, $N$")
        ax.set_ylabel("Count of authors")
        ax.set_yscale('log')
        return plt 



def SplitCountPlot(data):
    """
    """
    with pretty.Classic():
        fig = plt.figure(figsize = (12,8))    
        ax = fig.add_subplot(2, 2, 1)
        ax2 = fig.add_subplot(2, 2, 2)
        
        ax.scatter(data.query('n_coauthors > 0').n_coauthors,
                data.query('n_coauthors > 0').n_journals,
                alpha = 0.4, label = 'data')
        
        ax.plot(data.query('n_coauthors > 0').n_coauthors, data.query('n_coauthors > 0').n_coauthors, color = 'red', label = '45-deg line')
        
        ax2.hist(data.query('n_coauthors > 0').n_coauthors, bins = 50, alpha = .3, label = r"\#coauthors")    
        ax2.hist(data.query('n_coauthors > 0').n_journals, bins = 30, alpha = .5, label = r"\#journals")
        ax2.set_yscale('log')    
        
        ax.grid(which='minor', alpha=0.4, axis='y', linestyle='dotted')
        ax.grid(which='major', alpha=0.8, linestyle='dotted')

        ax2.grid(which='minor', alpha=0.4, axis='y', linestyle='dotted')
        ax2.grid(which='major', alpha=0.8, linestyle='dotted')    
        
        ax.annotate('$\mathbf{FIG.2.}$', xy=(0, 1.035), xycoords='axes fraction', ha='left',
                fontsize=18, annotation_clip=False)
        ax.annotate('$Relation \ between \ coauthor \ count \ and \ journal \ count$', xy=(0.195, 1.035), xycoords='axes fraction', ha='left',
                fontsize=18, annotation_clip=False)
        
        ax.set_xlabel("\# Coauthors")
        ax.set_ylabel("\# Journals")
            
        ax.legend()
        ax2.legend()
        
        return plt



def plotByFirstLetter(data):
    """
    """
    def math_formatter(x, pos):
        return "{}".format(x).replace(u"\u2212", "-")
    
    df = data.groupby('firstLetterIdx').agg(['mean', 'sem']).reset_index()
    df = df[df.firstLetterIdx != -1]
    
    df = df.iloc[:100]

    df['pubsup'] = df.pubs['mean'] + 1.96 * df.pubs['sem']
    df['pubslo'] = df.pubs['mean'] - 1.96 * df.pubs['sem']

    df['coauthup'] = df.n_coauthors['mean'] + 1.96 * df.n_coauthors['sem']
    df['coauthlo'] = df.n_coauthors['mean'] - 1.96 * df.n_coauthors['sem']


    with pretty.styles.Classic():
        fig = plt.figure(figsize = (12,8))    
        ax = fig.add_subplot(1, 1, 1)
        ax.minorticks_off()        
        ax.yaxis.set_major_formatter(FuncFormatter(math_formatter)) 
        
        ax.plot(df.firstLetterIdx, df.pubs['mean'], label = r'Avg. publications $N$')        
        ax.fill_between(df.firstLetterIdx, df['pubsup'], df['pubslo'], alpha = .2)

        ax.plot(df.firstLetterIdx, df.n_coauthors['mean'], label = r'Avg. coauthors, $N$')
        ax.fill_between(df.firstLetterIdx, df['coauthup'], df['coauthlo'], alpha = .2)

        ax.set_xticks([i for i in df.firstLetterIdx])
        ax.set_xticklabels([i for i in string.ascii_lowercase])    

        ax.annotate('$\mathbf{FIG.3.}$', xy=(0, 1.015), xycoords='axes fraction', ha='left',
                fontsize=18, annotation_clip=False)
        ax.annotate('$Author \ name \ rank \ and \ mean \ performance$', xy=(0.105, 1.015), xycoords='axes fraction', ha='left',
                fontsize=18, annotation_clip=False)

        ax.set_xlabel("First letter of name")
        ax.set_ylabel(r"$N$")

        ax.grid(which='major', alpha=0.8, linestyle='dotted')        
        ax.legend(loc = 'upper left')

        return plt
