"""
linearregression.py -> Script für Linear Regression an Aktiendaten
"""

from sklearn import preprocessing, cross_validation
from sklearn.linear_model import LinearRegression

import numpy as np

import pandas as pd
import pandas_datareader.data as web

import datetime


def get_data(stock: str) -> pd.DataFrame:
    """
    Gets historical stock data from Yahoo Finance API

    Parameters
    ----------
    stock : str
        Stock Symbol

    Returns
    -------
    pd.DataFrame
        Historical stock data
    """
    # defining starting and ending time
    start = datetime.datetime(2000, 1, 1)
    end = datetime.datetime.today()

    # getting historical data
    return web.DataReader(stock, 'yahoo', start, end)


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processes stock data

    Parameters
    ----------
    df : pd.DataFrame
        Historical stock data

    Returns
    -------
    pd.DataFrame
        Processed stock data
    """
    # difference between high and low
    df['HL_PCT'] = (df['High'] - df['Low']) / df['Adj Close'] * 100.0
    # overall change over the day
    df['PCT_change'] = (df['Adj Close'] - df['Open']) / df['Open'] * 100.0
    # 10d average
    df['10D_AVG'] = df['Adj Close'].rolling(window=10).mean()

    df = df[['Adj Close', 'HL_PCT', 'PCT_change', '10D_AVG', 'Volume']]

    # replacing every nan value
    df.fillna(value=-99999, inplace=True)

    return df


def train(df: pd.DataFrame) -> LinearRegression:
    """
    Trains Linear Regression model on given dataset

    Parameters
    ----------
    df : pd.DataFrame
        Historical stock data

    Returns
    -------
    LinearRegression
        Linear Regression model
    """
    df = process_data(df)

    # 5 day forecast
    df['Label'] = df['Adj Close'].shift(-5)
    df.dropna(inplace=True)

    # defining X and y for algorithm
    X = np.array(df.drop(['Label'], 1))
    y = np.array(df['Label'])

    # splitting dataset into training and testing data
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
        X, y, test_size=0.2)

    # training algorithm with as many threads as possible
    clf = LinearRegression(n_jobs=-1)
    clf.fit(X_train, y_train)

    # coefficient of determination (R2)
    confidence = clf.score(X_test, y_test)
    print(confidence)

    return clf


def predict(df: pd.DataFrame, classfier: LinearRegression) -> pd.DataFrame:
    """
    Predicts the future stock prices

    Parameters
    ----------
    df : pd.DataFrame
        Historical stock data
    classfier : LinearRegression
        Linear Regression model

    Returns
    -------
    pd.DataFrame
        Predicted stock price
    """
    # recent 5 days
    df = process_data(df)[-5:]

    # predicting price for the next 5 days
    return clf.predict(df)


if __name__ == '__main__':

    # getting data for Apple
    data = get_data('AAPL')

    # training and predicting
    clf = train(data)
    predicted = predict(data, clf)

    # printing prediction
    print(predicted)
