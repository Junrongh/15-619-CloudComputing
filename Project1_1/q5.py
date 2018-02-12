#!/usr/bin/env python3
import pandas as pd
import json
from csv import QUOTE_NONE


def main():
    """
    Please search and read the following docs to understand the starter code.

    pandas.read_table

        1) With 'squeeze=True', pandas.read_table returns a Series instead of a 
        DataFrame.

        2) Without 'quoting=QUOTE_NONE', the following records will be 
        interpreted to share the same title 'Wild_Bill_Hickok':
            "Wild_Bill"_Hickok	63
            Wild_Bill_Hickok	40

        3) Without 'keep_default_na=False', the following records will be 
        interpreted to numpy.nan (Not a Number):
            NaN 13

    pandas.Index.tolist
        to convert the indexes to a list


    TODO: 
    * Slice the top 3 articles
    * Convert the indexes as a list
    * Dump the list as a JSON array
    * Print the JSON array to StdOut
    """
    navalues=['nan']
    s = pd.read_table('output', header=None, index_col=0, squeeze=True,
                      quoting=QUOTE_NONE, keep_default_na=False,
                      na_values=navalues, encoding='utf-8')
    d = pd.Index.tolist(s.sort_values(ascending = False).head(3).index)
    print(json.dumps(d))


if __name__ == "__main__":
    main()
