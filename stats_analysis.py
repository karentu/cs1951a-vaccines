import numpy as np
import pandas as pd
from scipy import stats
from sklearn import linear_model
from sklearn.linear_model import LinearRegression

from ml_analysis import preprocess_features, all_features, labels
import matplotlib.pyplot as plt
import seaborn as sns

# Split data into two groups based on the label
# label_index: an integer marking the indice of the label (in the labels list) to split on
def split_data_based_on_label(df, label_index):
    label = labels[label_index]
    label_data = df[label].values
    # To split the data based on median
    median = np.percentile(label_data, 50)
    print('The 50th percentile of the label is: %f' % median)

    df_low = df.loc[df[label] <= median]
    df_high = df.loc[df[label] > median]

    return df_low, df_high

def split_data_based_on_feature(df, feature):
    feature_data = df[feature].values
    # To split the data based on median
    median = np.percentile(feature_data, 50)
    print(('The 50th percentile of the feature ' + feature + 'is: %f') % median)

    column_name = 'low ' + feature
    df[column_name] = df[feature] <= median

    return df

def t_test(x, y):
    x = (x - np.min(x)) / (np.max(x) - np.min(x))
    y = (y - np.min(y)) / (np.max(y) - np.min(y))

    x_mean = np.mean(x)
    y_mean = np.mean(y)
    n_1 = len(x)
    n_2 = len(y)
    s_1 = np.std(x)
    s_2 = np.std(y)
    dof = n_1 + n_2 - 2
    part_1 = (((n_1 - 1) * s_1) + ((n_2 - 1) * s_2)) / dof
    part_2 = (1 / n_1) + (1 / n_2)
    t_score = (x_mean - y_mean) / (np.sqrt(part_1 * part_2))
    return t_score, dof

def scatter_plot_by_feature_tier(df, label_index):
    label = labels[label_index]
    # can comment out
    df = df.groupby(['school_district']).mean()
    for feature in all_features:
        # comment out if not grouping by school_district
        if feature == 'school_district':
            continue
        new_df = split_data_based_on_feature(df, feature)
        fig, ax = plt.subplots()
        ax = sns.scatterplot(x=feature, y=label, hue="low "+feature, data=new_df)

        df_low = df.loc[new_df["low "+feature] == True]
        df_high = df.loc[new_df["low "+feature] == False]

        low_x = df_low[feature].values
        low_x = np.reshape(low_x, (len(low_x), 1))
        low_y = df_low[label].values
        low_y = np.reshape(low_y, (len(low_y), 1))
        reg_1 = LinearRegression().fit(low_x, low_y)
        coef_1, intercept_1 = reg_1.coef_[0], reg_1.intercept_
        low_range = np.arange(np.min(low_x) - 1, np.max(low_x) + 1, (np.max(low_x) - np.min(low_x)) / 10)
        line_1 = [(coef_1[0] * x + intercept_1[0]) for x in low_range]
        high_x = df_high[feature].values
        high_x = np.reshape(high_x, (len(high_x), 1))
        high_y = df_high[label].values
        high_y = np.reshape(high_y, (len(high_y), 1))
        reg_2 = LinearRegression().fit(high_x, high_y)
        coef_2, intercept_2 = reg_2.coef_[0], reg_2.intercept_
        high_range = np.arange(np.min(high_x) - 1, np.max(high_x) + 1, (np.max(high_x) - np.min(high_x)) / 10)
        line_2 = [(coef_2[0] * x + intercept_2[0]) for x in high_range]
        plt.plot(low_range, line_1, c='orange', label='low '+feature +' best fit')
        plt.plot(high_range, line_2, c='b', label='low '+feature +' best fit')
        plt.savefig('stats_result/'+feature+'_scatterplot')



def main():
    df = preprocess_features()
    df_low, df_high = split_data_based_on_label(df, 0)

    # whole test
    # label_data = df[labels[0]].values
    # for feature in all_features:
    #     feature_data = df[feature].values
    #     t_score, dof = t_test(feature_data, label_data)
    #     print('t-test for feature ' + feature + ' (without split)')
    #     print('t_score is %f, degree of freedom is %d' % (t_score, dof))
    # # split test
    # label_data = df_low[labels[0]].values
    # for feature in all_features:
    #     feature_data = df_low[feature].values
    #     t_score, dof = t_test(feature_data, label_data)
    #     print('t-test for feature ' + feature + ' (low)')
    #     print('t_score is %f, degree of freedom is %d' % (t_score, dof))
    # label_data = df_high[labels[0]].values
    # for feature in all_features:
    #     feature_data = df_high[feature].values
    #     t_score, dof = t_test(feature_data, label_data)
    #     print('t-test for feature ' + feature + ' (high)')
    #     print('t_score is %f, degree of freedom is %d' % (t_score, dof))

    # compare two splits
    for feature in all_features:
        x = df_low[feature].values
        y = df_high[feature].values
        t_score, dof = t_test(x, y)
        pval = stats.t.sf(np.abs(t_score), dof)
        print('t-test for feature ' + feature)
        print('t_score is %f, degree of freedom is %d, one-tail p value is %f' % (t_score, dof, pval))

    # Can also check p-value at:
    # https://www.socscistatistics.com/pvalues/tdistribution.aspx
    # https://www.graphpad.com/quickcalcs/pValue1/

    # scatter_plot_by_feature_tier(df, 0)

if __name__ == "__main__":
    main()
