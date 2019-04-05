import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns

class VisualAnalysis(object):
    def __init__(self):
        self.df_school = pd.read_csv('./complete_cleaned.csv')
        self.df_county = pd.read_csv('./county_stats.csv')

    # Calculate average vaccination rates among counties
    def calc_average_county(self):
        counties = self.df_county['county'].values
        counties = [county_name[:-7] for county_name in counties]

        # four counties do not have schools: Grays Harbor, Pend Oreille, San Juan, Walla Walla
        average_dict = {}
        for county in counties:
            total = self.df_school.loc[self.df_school['county'] == county]
            if total.size != 0:
                immunization_rate = total['all_immunizations'] / total['k12_enrollment']
                average = immunization_rate.mean()
                average_dict[county] = average
        return average_dict

    def scatter_plot_county(self):
        average_county = self.calc_average_county()
        delete_index = []
        for index, row in self.df_county.iterrows():
            if row['county'][:-7] not in average_county:
                delete_index.append(index)
        cleaned_county = self.df_county.drop(delete_index)
        cleaned_county['immunization_rate'] = list(average_county.values())

        county_info = self.df_county.columns.values[2:]
        for i in county_info:
            data = cleaned_county[[i, 'immunization_rate']]
            fig, ax = plt.subplots()
            ax = sns.scatterplot(x=i, y="immunization_rate", data=data)
            plt.savefig('./visualization/' + i + '_scatterplot.png')

def main():
    va = VisualAnalysis()
    va.scatter_plot_county()

if __name__ == "__main__":
    main()
