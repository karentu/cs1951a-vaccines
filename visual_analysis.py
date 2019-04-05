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

    #
    #
    # def plot_distributions(self):
    #     # plot k12 enrollment of schools
    #     enrollment = self.df_school['k12_enrollment'].values
    #     fig, ax = plt.subplots()
    #     ax.set_title('k12 enrollment')
    #     ax.hist(enrollment, bins=50)
    #     plt.savefig('./data_plots/k12_enrollment_distribution.png')
    #
    #     # plot percentage of all_immunizations
    #     percentage = (self.df_school['all_immunizations'] / self.df_school['k12_enrollment']).values
    #     fig, ax = plt.subplots()
    #     ax.set_title('immunization rate')
    #     ax.hist(percentage, bins=50)
    #     plt.savefig('./data_plots/immunization_rate_distribution.png')
    #
    #     # plot county info
    #     county_info = self.df_county.columns.values[2:]
    #     bins = [9, 12, 20, 20, 20, 20, 20, 20, 20, 20, 20]
    #     pair = zip(county_info, bins)
    #     for column, num_bin in pair:
    #         data = self.df_county[column].values
    #         fig, ax = plt.subplots()
    #         ax.set_title(column)
    #         ax.hist(data, bins=num_bin, ec='black')
    #         plt.savefig('./data_plots/' + column + '_distribution.png')
    #
    #
    # def plot_correlation_heatmap(self):
    #     # correlation among county's independent variables
    #     fig, ax = plt.subplots(figsize=(20, 10))
    #     sns.set()
    #     county_info = self.df_county.columns.values[2:]
    #     f = self.df_county.loc[:, county_info].corr()
    #     ax = sns.heatmap(f, annot=True)
    #     plt.subplots_adjust(left=0.25, bottom=0.36, right=1.00,
    #                         top=0.98)
    #     plt.savefig('./data_plots/county_correlation_heatmap.png')
    #
    # def describe_school(self):
    #     df_school_info = self.df_school[['k12_enrollment', 'all_immunizations']]
    #     print(df_school_info.describe())
    #
    # def describe_county(self):
    #     # for printing on the command line
    #     df_county_info_1 = self.df_county[self.df_county.columns[2:8]]
    #     df_county_info_2 = self.df_county[self.df_county.columns[8:]]
    #     print(df_county_info_1.describe())
    #     print(df_county_info_2.describe())

def main():
    va = VisualAnalysis()
    va.scatter_plot_county()

if __name__ == "__main__":
    main()
