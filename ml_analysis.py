import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scipy import stats
from sklearn.preprocessing import PolynomialFeatures


all_features = ['rural_urban', 'urban_influence', 'high_school_degree_percent',
            'politics', 'percent_pov_child', 'percent_pov_all', 'employment_rate',
            'med_household_income_2017', 'white_county', 'white_school', 'grade_span',
            'male_percent', 'num_free_reduced_meals', 'total_percent_absences',
            'low_income_absence_percent', 'school_district']

multi_regression_features_shortened = ['high_school_degree_percent',
                                       'percent_pov_child',
                                       'employment_rate',
                                       'white_county',
                                       'white_school',
                                       'total_percent_absences',
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

def singleLinearRegression(df):
    for feature in all_features:
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
        print(feature + " results:")
        print('Intercept: %f, Coefficient: %f' % (lm.intercept_,lm.coef_))
        print('Training R-Squared: %f' % train_r_squared)
        print('Training MSE: %f' % train_mse)
        print('Testing MSE: %f' % test_mse)

def multipleLinearRegression(df):
    # change all_features to different feature list for different ML analysis
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

    train_r_squared = lm.score(X_train, y_train)
    train_mse = mean_squared_error(y_train, lm.predict(X_train))
    test_mse = mean_squared_error(y_test, lm.predict(X_test))
    print('Training R-Squared: %f' % train_r_squared)
    print('Training MSE: %f' % train_mse)
    print('Testing MSE: %f' % test_mse)


def linearCrossTerms(df):
    # change all_features to different feature list for different ML analysis
    X = df[all_features].values
    y = df[labels].values
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.1,
        shuffle=True
    )

    poly = PolynomialFeatures(interaction_only=True)
    transformed = poly.fit_transform(X_train)
    lm = linear_model.LinearRegression().fit(transformed, y_train)

    params = np.append(lm.intercept_, lm.coef_)
    predictions = lm.predict(transformed)

    newX = np.append(np.ones((len(transformed), 1)), transformed, axis=1)
    MSE = (sum((y_train - predictions) ** 2)) / (len(newX) - len(newX[0]))

    var_b = MSE * (np.linalg.pinv(np.dot(newX.T, newX)).diagonal())
    sd_b = np.sqrt(var_b)
    ts_b = params / sd_b

    p_values = [2 * (1 - stats.t.cdf(np.abs(i), (len(newX) - 1))) for i in ts_b]

    myDF3 = pd.DataFrame()
    myDF3["Coefficients"],myDF3["Standard Errors"],myDF3["t values"],myDF3["Probabilites"] = [params,sd_b,ts_b,p_values]
    print(myDF3)

    train_r_squared = lm.score(transformed, y_train)
    train_mse = mean_squared_error(y_train, lm.predict(transformed))
    test_transformed = poly.fit_transform(X_test)
    test_mse = mean_squared_error(y_test, lm.predict(X_test))
    print('Training R-Squared: %f' % train_r_squared)
    print('Training MSE: %f' % train_mse)
    print('Testing MSE: %f' % test_mse)


def main():
    df = preprocess_features()
    print(df['immunization_rate'])

    singleLinearRegression(df)
    multipleLinearRegression(df)
    #linearCrossTerms(df)


if __name__ == "__main__":
    main()
