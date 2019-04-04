import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

class DescribeData(object):
    def __init__(self):
        self.df_school = pd.read_csv('./complete_cleaned.csv')
        self.df_county = pd.read_csv('./county_stats.csv')

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

    def describe_school(self):
        df_school_info = self.df_school[['k12_enrollment', 'all_immunizations']]
        print(df_school_info.describe())

    def describe_county(self):
        df_county_info = self.df_county[self.df_county.columns[2:]]
        print(df_county_info.describe())

def main():
    describe = DescribeData()
    #describe.describe_school()
    #describe.describe_county()
    #describe.box_plot_school()
    describe.plot_distributions()


if __name__ == "__main__":
    main()
