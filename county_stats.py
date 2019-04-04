import numpy as np
import pandas as pd

def calculate_stats():
    df = pd.read_csv('./county.csv')

    # convert string to numbers
    df['med_household_income_2017'] = df['med_household_income_2017'].str.replace('$','')
    string_columns = ['high_school', 'clinton', 'trump', 'med_household_income_2017']
    for column in string_columns:
        df[column] = pd.to_numeric(df[column].str.replace(',',''))

    df['high_school_degree_percent'] = (1 - (df['high_school'] / df['totalPop'])).multiply(100).round(1)
    # 0 for Democrat and 1 for Republican
    df['politics'] = (df['clinton'] / (df['clinton'] + df['trump'])).round(2)
    df['employment_rate_2017'] = (df['employed_2017'] / df['labor_total_2017']).multiply(100).round(1)

    df_stats = df[['id', 'county', 'rural_urban', 'urban_influence', 'high_school_degree_percent',
                   'politics', 'percent_pov_all', 'percent_pov_child', 'employment_rate_2017',
                   'med_household_income_2017', 'medHHIncome_percent_state_2017',
                   'white', 'whiteAlone']]
    df_stats.to_csv('county_stats.csv')

def main():
    calculate_stats()

if __name__ == "__main__":
    main()
