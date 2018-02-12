#!/usr/bin/env python3
import pandas as pd
import sys
from csv import QUOTE_NONE


def main():
    """
    Please search and read the docs of the following methods.
    
    pandas.read_csv
        to read CSV (comma-separated) file into DataFrame
        
    pandas.DataFrame.merge
        to merge DataFrame objects by performing a database-style join operation
        specify the field "Article" to join on
    
    pandas.DataFrame.to_csv  
        to write DataFrame to a comma-separated values (csv) file
        set path_or_buf=sys.stdout to write the output to StdOut
    
    Alabama,"United_States_presidential_election_in_Alabama,_2016",9,109
    """
    navalues=['nan']
    pageview_df = pd.read_table('output', names=['Article', 'Pageviews'],
                                header=None, quoting=QUOTE_NONE, keep_default_na=False,
                                na_values=navalues, encoding='utf-8')
    races_df = pd.read_csv('races.csv')
    result = pd.merge(races_df,pageview_df,how='left',on=['Article'])
    r = result.to_csv(index=False)
    print(r)


if __name__ == "__main__":
    main()
