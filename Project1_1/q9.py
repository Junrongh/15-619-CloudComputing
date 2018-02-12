#!/usr/bin/env python3
import numpy as np
import pandas as pd
import re
import sys
from csv import QUOTE_NONE


def get_year(article):
    """
    Use regex capturing groups to convert the article and return the year 
    if it ends with "_(yyyy_film)", otherwise return np.nan
    
    this is the only function you need to implement
    
    :param article: the article
    :return: the year or np.nan
    """
    if re.search('_\(\d{4}_film\)$', article):
        a = article[len(article) - 10:len(article) - 6]
        # a = re.search(r'(\d{4})_film', article).group(1)
        return a
    else:
        return np.nan


def main():
    """
    Please search and read the docs of the following methods.
    
    pandas.Index.map
        to apply mapper function to an index
        
    pandas.Series.rank
        to compute the ranking, specific parameters are needed
        
    pandas.Series.astype
        to cast the data type (to int)
        
    pandas.Series.to_json
        to convert the series to a JSON string
    """
    navalues=['nan']
    s = pd.read_table('output', header=None, index_col=0, squeeze=True,
                  quoting=QUOTE_NONE, keep_default_na=False,
                  na_values=navalues, encoding='utf-8')

    # convert each article to the year

    s.index = s.index.map(get_year)
    # group by, sum and rank the years
    # NA groups in GroupBy are automatically excluded
    ranking = s.groupby(s.index).sum().rank(method='min', ascending=False).astype(int)


    # convert to JSON and write to StdOut
    ranking.to_json(sys.stdout)


if __name__ == "__main__":
    main()
