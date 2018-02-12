#!/usr/bin/env python3
import pandas as pd
from csv import QUOTE_NONE


def main():
    """
    Please search and read the docs of the following methods.
    
    pandas.Series.loc or pandas.Series.filter
        to filter the articles of the senators
        
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

    with open('senators.txt') as f:
        senators = f.read().splitlines();
        c = s.loc[senators];
        d = c.rank(ascending=False,method='min').astype('int64').to_json()
        print(d)

if __name__ == "__main__":
    main()
