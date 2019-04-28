import numpy as np
import pandas as pd
from scipy import stats

from ml_analysis import preprocess_features, all_features, labels

# Split data into two groups based on the label
# label_index: an integer marking the indice of the label (in the labels list) to split on
def split_data(df, label_index):
    label = labels[label_index]
    label_data = df[label].values
    # To split the data based on median
    median = np.percentile(label_data, 50)
    print('The 50th percentile of the label is: %f' % median)

    df_low = df.loc[df[label] < median]
    df_high = df.loc[df[label] >= median]

    return df_low, df_high

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

def main():
    df = preprocess_features()
    df_low, df_high = split_data(df, 0)

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

if __name__ == "__main__":
    main()
