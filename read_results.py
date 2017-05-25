# This is a Python port of gerrymander_readresults.m:
import pandas as pd
def read_results(year, states):
    # Let's read the csv file into a pandas dataframe
    df = pd.read_csv('House_1898_2014_voteshares_notext.csv', header = None)
    # Let's name the columns
    df.columns = ['Year', 'State', 'District', 'D_voteshare', 'Incumbent', 'Winner']
    # We'll only extract those with the correct year
    year_df = df[df['Year'] == year]
    # Now we'll just take the values with the correct states
    result = year_df[year_df['State'].isin(states)]
    # Drop the 'Year' column from the dataframe
    del result['Year']
    # Return the remaining dataframe
    return result