import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns

class DescribeData(object):
    def __init__(self):
        self.df_school = pd.read_csv('./complete_cleaned.csv')
        self.df_county = pd.read_csv('./county_stats.csv')
        self.merged = pd.read_csv('./merged_county_stats.csv')

    def box_plot_school(self):
        school_enrollment = self.df_school['k12_enrollment'].values
        fig, ax = plt.subplots()
        ax.set_title('k12 enrollment of schools')
        ax.boxplot(school_enrollment, flierprops=dict(markerfacecolor="g", marker="D"))
        plt.savefig('./data_plots/k12_enrollment_box_plot.png')


    def plot_distributions(self):
        # plot k12 enrollment of schools
        enrollment = self.df_school['k12_enrollment'].values
        fig, ax = plt.subplots()
        ax.set_title('k12 enrollment')
        ax.hist(enrollment, bins=50)
        plt.savefig('./data_plots/k12_enrollment_distribution.png')

        # plot percentage of all_immunizations
        percentage = (self.df_school['all_immunizations'] / self.df_school['k12_enrollment']).values
        fig, ax = plt.subplots()
        ax.set_title('immunization rate')
        ax.hist(percentage, bins=50)
        plt.savefig('./data_plots/immunization_rate_distribution.png')

        # plot county info
        county_info = self.df_county.columns.values[2:]
        bins = [9, 12, 20, 20, 20, 20, 20, 20, 20, 20, 20]
        pair = zip(county_info, bins)
        for column, num_bin in pair:
            data = self.df_county[column].values
            fig, ax = plt.subplots()
            ax.set_title(column)
            ax.hist(data, bins=num_bin, ec='black')
            plt.savefig('./data_plots/' + column + '_distribution.png')


    def plot_correlation_heatmap(self):
        # correlation among county's independent variables
        fig, ax = plt.subplots(figsize=(20, 10))
        sns.set()
        county_info = self.df_county.columns.values[2:]
        f = self.df_county.loc[:, county_info].corr()
        ax = sns.heatmap(f, annot=True)
        plt.subplots_adjust(left=0.25, bottom=0.36, right=1.00,
                            top=0.98)
        plt.savefig('./data_plots/county_correlation_heatmap.png')

        # correlation among different vaccination rates
        immunization = ['all_immunizations', 'diphtheria_tetanus','pertussis','mmr','polio','hepatitisB','varicella']
        temp_df = self.df_school.copy()
        for i in immunization:
            temp_df[i+'_rate'] = temp_df[i] / temp_df['k12_enrollment']

        immune_rate_columns = [(x+'_rate') for x in immunization]
        fig, ax = plt.subplots(figsize=(15, 10))
        sns.set()
        f = temp_df.loc[:, immune_rate_columns].corr()
        ax = sns.heatmap(f, annot=True)
        plt.subplots_adjust(left=0.19, bottom=0.25, right=0.95, top=0.94)
        plt.savefig('./data_plots/vaccination_correlation_heatmap.png')

    def plot_combined_correlation_heatmap(self):
        # correlation among county's independent variables
        fig, ax = plt.subplots(figsize=(20, 10))
        sns.set()
        merged_info = self.merged.columns.values[2:]
        f = self.merged.loc[:, merged_info].corr()
        ax = sns.heatmap(f, annot=True)
        plt.subplots_adjust(left=0.25, bottom=0.36, right=1.00,
                            top=0.98)
        # plt.show()
        plt.savefig('./visualization/final_correlation_heatmap.png')

    def describe_school(self):
        df_school_info = self.df_school[['k12_enrollment', 'all_immunizations']]
        print(df_school_info.describe())

    def describe_county(self):
        # for printing on the command line
        df_county_info_1 = self.df_county[self.df_county.columns[2:8]]
        df_county_info_2 = self.df_county[self.df_county.columns[8:]]
        print(df_county_info_1.describe())
        print(df_county_info_2.describe())

def main():
    describe = DescribeData()
    # describe.describe_school()
    # describe.describe_county()
    # describe.box_plot_school()
    # describe.plot_distributions()
    # describe.plot_correlation_heatmap()
    describe.plot_combined_correlation_heatmap()

if __name__ == "__main__":
    main()
