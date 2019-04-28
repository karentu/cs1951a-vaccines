import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder, normalize
from sklearn.model_selection import train_test_split

from sklearn import dummy, linear_model, svm
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from scipy import stats
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
from sklearn.neural_network import MLPRegressor


all_features = ['rural_urban', 'urban_influence', 'high_school_degree_percent',
            'politics', 'percent_pov_child', 'percent_pov_all', 'employment_rate',
            'med_household_income_2017', 'white_county', 'white_school', 'grade_span',
            'male_percent', 'num_free_reduced_meals', 'total_percent_absences',
            'low_income_absence_percent', 'school_district']

multi_regression_features_shortened = ['high_school_degree_percent',
                                       'percent_pov_child',
                                       'employment_rate',
                                       'med_household_income_2017',
                                       'white_county',
                                       'white_school',
                                       'grade_span',
                                       'num_free_reduced_meals',
                                       'total_percent_absences',
                                       'low_income_absence_percent',
                                       'school_district']

labels = ['immunization_rate']

def preprocess_features():
    df = pd.read_csv('./complete_with_school_cleaned.csv')

    df['med_household_income_2017'] = df['med_household_income_2017'].str.replace('$','')
    string_columns = ['high_school', 'clinton', 'trump', 'med_household_income_2017',
                      'employed_2015', 'labor_total_2015', 'labor_total_2016',
                      'employed_2016']
    for column in string_columns:
        df[column] = pd.to_numeric(df[column].str.replace(',',''))
    percent_columns = ['total_percent_absences', 'low_income_absence_percent']
    for column in percent_columns:
        df[column] = pd.to_numeric(df[column].str.replace('%',''))

    df['high_school_degree_percent'] = (1 - (df['high_school'] / df['totalPop'])).multiply(100).round(1)
    df['politics'] = (df['clinton'] / (df['clinton'] + df['trump'])).round(2)
    # corresponding year
    df['employment_rate'] = (df['employed_2015'] / df['labor_total_2015']).multiply(100).round(1)
    df.loc[df['school_year'] == 2016, 'employment_rate'] = (df['employed_2016'] /
                                                            df['labor_total_2016']).multiply(100).round(1)
    df.loc[df['school_year'] == 2017, 'employment_rate'] = (df['employed_2017'] /
                                                            df['labor_total_2017']).multiply(100).round(1)


    df['white_county'] = df['white']
    df['white_school'] = (df['school_white'] / df['total_enrollment']).multiply(100).round(1)
    df['grade_span'] = df['end_grade'] - df['start_grade']
    df['male_percent'] = (df['male'] / df['total_enrollment']).multiply(100).round(1)

    label_encoder = LabelEncoder()
    df['school_district'] = np.array(label_encoder.fit_transform(df['school_district'].values))

    df['immunization_rate'] = (df['all_immunizations'] / df['k12_enrollment']).multiply(100).round(1)
    return df[all_features + labels]

def feature_selection(df, method, k):
    X = df[all_features].values
    y = np.ravel(df[labels].values)
    selector = SelectKBest(method, k=k)
    X_selected = selector.fit_transform(X, y)
    feature_indices = selector.get_support(indices=True)
    selected_features = []
    for index in feature_indices:
        selected_features.append(all_features[index])
    print(selected_features)
    return X_selected

def singleLinearRegression(df):
    for feature in all_features:
        single_r_square = 0
        single_train_mse = 0
        single_test_mse = 0
        for i in range(5):
            X = df[feature].values
            X = np.reshape(X, (-1,1))
            y = df[labels].values
            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.1,
                shuffle=True
            )

            lm = LinearRegression().fit(X_train, y_train)

            train_r_squared = lm.score(X_train, y_train)
            train_mse = mean_squared_error(y_train, lm.predict(X_train))
            test_mse = mean_squared_error(y_test, lm.predict(X_test))
            single_r_square += train_r_squared
            single_train_mse += train_mse
            single_test_mse += test_mse
        print(feature + " results:")
        print('Training R-Squared: %f' % (single_r_square / 5))
        print('Training MSE: %f' % (single_train_mse / 5))
        print('Testing MSE: %f' % (single_test_mse / 5))

def getMultipleLinearRegressionP(df):
    X = df[all_features].values
    y = df[labels].values

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.1,
        shuffle=True
    )

    lm = LinearRegression().fit(X_train, y_train)
    params = np.append(lm.intercept_,lm.coef_)
    predictions = lm.predict(X_train)

    newX = np.append(np.ones((len(X_train),1)), X_train, axis=1)
    MSE = (sum((y_train-predictions)**2))/(len(newX)-len(newX[0]))

    var_b = MSE*(np.linalg.inv(np.dot(newX.T,newX)).diagonal())
    sd_b = np.sqrt(var_b)
    ts_b = params/ sd_b

    p_values =[2*(1-stats.t.cdf(np.abs(i),(len(newX)-1))) for i in ts_b]

    myDF3 = pd.DataFrame()
    myDF3["Coefficients"],myDF3["Standard Errors"],myDF3["t values"],myDF3["Probabilites"] = [params,sd_b,ts_b,p_values]
    print(myDF3)

def multipleLinearRegression(X, y):
    multi_r_sqaure = 0
    multi_train_mse = 0
    multi_test_mse = 0
    for i in range(20):
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.1,
            shuffle=True
        )

        lm = LinearRegression().fit(X_train, y_train)

        train_r_squared = lm.score(X_train, y_train)
        train_mse = mean_squared_error(y_train, lm.predict(X_train))
        test_mse = mean_squared_error(y_test, lm.predict(X_test))
        multi_r_sqaure += train_r_squared
        multi_train_mse += train_mse
        multi_test_mse += test_mse

    print('Training R-Squared: %f' % (multi_r_sqaure / 20))
    print('Training MSE: %f' % (multi_train_mse / 20))
    print('Testing MSE: %f' % (multi_test_mse / 20))

def svm(X, y, kernel):
    if kernel == 'poly':
        print('normalizing data')
        X = np.array([(x - min(x)) / (max(x) - min(x)) for x in X])
        y = y / 100

    svm_r_sqaure = 0
    svm_train_mse = 0
    svm_test_mse = 0
    for i in range(3):
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y.ravel(),
            test_size=0.1,
            shuffle=True
        )

        clf = SVR(kernel=kernel,
                  degree=3,
                  gamma='auto').fit(X_train, y_train)

        train_r_squared = clf.score(X_train, y_train)
        train_mse = mean_squared_error(y_train, clf.predict(X_train))
        test_mse = mean_squared_error(y_test, clf.predict(X_test))
        svm_r_sqaure += train_r_squared
        svm_train_mse += train_mse
        svm_test_mse += test_mse

    print('Training R-Squared: %f' % (svm_r_sqaure / 3))
    print('Training MSE: %f' % (svm_train_mse / 3))
    print('Testing MSE: %f' % (svm_test_mse / 3))

def neural_network(X, y):
    nn_r_sqaure = 0
    nn_train_mse = 0
    nn_test_mse = 0
    for i in range(5):
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y.ravel(),
            test_size=0.1,
            shuffle=True
        )

        clf = MLPRegressor(hidden_layer_sizes=(8,),
                           activation="tanh",
                           alpha=0.001,
                           learning_rate_init=0.001,
                           max_iter=2000).fit(X_train, y_train)

        train_r_squared = clf.score(X_train, y_train)
        train_mse = mean_squared_error(y_train, clf.predict(X_train))
        test_mse = mean_squared_error(y_test, clf.predict(X_test))
        nn_r_sqaure += train_r_squared
        nn_train_mse += train_mse
        nn_test_mse += test_mse

    print('Training R-Squared: %f' % (nn_r_sqaure / 5))
    print('Training MSE: %f' % (nn_train_mse / 5))
    print('Testing MSE: %f' % (nn_test_mse / 5))

def baseLine(df):
    dummy_train_r2 = 0
    dummy_train_mse = 0
    dummy_test_mse = 0
    for i in range(5):
        base_line_predictor = dummy.DummyRegressor(strategy="mean")
        X = df[all_features].values
        y = df[labels].values
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.1,
            shuffle=True
        )

        base_line_predictor.fit(X_train, y_train)
        train_r_squared = base_line_predictor.score(X_train, y_train)
        train_mse = mean_squared_error(y_train, base_line_predictor.predict(X_train))
        test_mse = mean_squared_error(y_test, base_line_predictor.predict(X_test))
        dummy_train_r2 += train_r_squared
        dummy_train_mse += train_mse
        dummy_test_mse += test_mse
    print('Training R-Squared: %f' % (dummy_train_r2 / 5))
    print('Training MSE: %f' % (dummy_train_mse / 5))
    print('Testing MSE: %f' % (dummy_test_mse / 5))


def main():
    df = preprocess_features()

    # baseLine(df)

    # print('Top 1 Features selected by F-regression:')
    # feature_selection(df, f_regression, 1)
    # print('Top 3 Features selected by F-regression:')
    # feature_selection(df, f_regression, 3)
    print('Top 5 Features selected by F-regression:')
    f_regression_X = feature_selection(df, f_regression, 5)
    # print('Top 1 Features selected by mutual info regression:')
    # feature_selection(df, mutual_info_regression, 1)
    # print('Top 3 Features selected by mutual info regression:')
    # feature_selection(df, mutual_info_regression, 3)
    print('Top 5 Features selected by mutual info regression:')
    mutual_info_X = feature_selection(df, mutual_info_regression, 5)

    # singleLinearRegression(df)
    # getMultipleLinearRegressionP(df)
    # print('Multi-linear regression on all features:')
    # multipleLinearRegression(df[all_features].values, df[labels].values)
    # print('Multi-linear regression on features selected by p-values:')
    # multipleLinearRegression(df[multi_regression_features_shortened].values, df[labels].values)
    # print('Multi-linear regression on features selected by sklearn (f score):')
    # multipleLinearRegression(f_regression_X, df[labels].values)
    # print('Multi-linear regression on features selected by sklearn (mutual info):')
    # multipleLinearRegression(mutual_info_X, df[labels].values)

    # print('SVM (rbf) regression on all features:')
    # svm(df[all_features].values, df[labels].values, 'rbf')
    # print('SVM (rbf) regression on features selected by p-values:')
    # svm(df[multi_regression_features_shortened].values, df[labels].values, 'rbf')
    # print('SVM (rbf) regression on features selected by sklearn (f score):')
    # svm(f_regression_X, df[labels].values, 'rbf')
    # print('SVM (rbf) regression on features selected by sklearn (mutual info):')
    # svm(mutual_info_X, df[labels].values, 'rbf')

    # print('Neural Network regression on all features:')
    # neural_network(df[all_features].values, df[labels].values)
    # print('Neural Network regression on features selected by p-values:')
    # neural_network(df[multi_regression_features_shortened].values, df[labels].values)
    # print('Neural Network regression on features selected by sklearn (f score):')
    # neural_network(f_regression_X, df[labels].values)
    # print('Neural Network regression on features selected by sklearn (mutual info):')
    # neural_network(mutual_info_X, df[labels].values)

    # print('SVM (poly) regression on all features:')
    # svm(df[all_features].values, df[labels].values, 'poly')
    # print('SVM (poly) regression on features selected by p-values:')
    # svm(df[multi_regression_features_shortened].values, df[labels].values, 'poly')
    # print('SVM (poly) regression on features selected by sklearn (f score):')
    # svm(f_regression_X, df[labels].values, 'poly')
    # print('SVM (poly) regression on features selected by sklearn (mutual info):')
    # svm(mutual_info_X, df[labels].values, 'poly')


if __name__ == "__main__":
    main()
