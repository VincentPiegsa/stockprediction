"""
linear.py -> Algorithmus für Linear Regression an Aktien Daten
Attributes:
    PATH (str): Speicherpfad
"""
import pandas as pd
import numpy as np
import pickle
import os
import datetime
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from core import logger

PATH = './core/linear-models/'

def run(data, name):
    """Vorhersage des Models
    
    Args:
        data (np.array): Daten
        name (str): Datenname
    
    Returns:
        np.array: Vorhersage
    """
    if os.path.isfile('{}/{}-{}.model'.format(PATH, name, datetime.date.today())):

        logger.info('Predicting data for {}.'.format(name))
        return predict(data, name)

    else:

        logger.info('Training model for {}.'.format(name))
        train(data, name)

        logger.info('Predicting data for {}.'.format(name))
        return predict(data, name)


def train(data, name, forecast=5):
    """Trainiert das Model
    
    Args:
        data (np.array): Daten
        name (str): Datenname
        forecast (int, optional): Anzahl der vorhergesagten Tage
    """
    forecast_col = 'Adj Close'
    df = data[['Open', 'High', 'Low', 'Adj Close', 'Volume']]

    df['HL_PCT'] = (df['High'] - df['Low']) / df['Adj Close'] * 100.0
    df['PCT_CHANGE'] = (df['Adj Close'] - df['Open']) / df['Open'] * 100.0
    df['ROLLING_AVG'] = df['Adj Close'].rolling(window=10).mean()

    df = df[['Adj Close', 'HL_PCT', 'PCT_CHANGE', 'ROLLING_AVG', 'Volume']]
    df.fillna(value=-99999, inplace=True)

    df['label'] = df[forecast_col].shift(-forecast)
    df.dropna(inplace=True)

    X = np.array(df.drop(['label'], 1))
    y = np.array(df['label'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01)

    classifier = LinearRegression(n_jobs=-1)
    classifier.fit(X_train, y_train)

    with open('{}/{}-{}.model'.format(PATH, name, datetime.date.today()), 'wb') as file:
        pickle.dump(classifier, file)


def predict(data, name):
    """Vorhersage des Models
    
    Args:
        data (np.array): Daten
        name (str): Datenname
    
    Returns:
        np.array: Vorhersage
    """
    with open('{}/{}-{}.model'.format(PATH, name, datetime.date.today()), 'rb') as file:
        classifier = pickle.load(file)

    forecast_col = 'Adj Close'
    df = data[['Open', 'High', 'Low', 'Adj Close', 'Volume']]

    df['HL_PCT'] = (df['High'] - df['Low']) / df['Adj Close'] * 100.0
    df['PCT_CHANGE'] = (df['Adj Close'] - df['Open']) / df['Open'] * 100.0
    df['ROLLING_AVG'] = df['Adj Close'].rolling(window=10).mean()

    df = df[['Adj Close', 'HL_PCT', 'PCT_CHANGE', 'ROLLING_AVG',  'Volume']]
    df.fillna(value=-99999, inplace=True)

    prediction = classifier.predict(df[-5:])
    dates = [df.index[-1] + datetime.timedelta(days=days) for days in range(1, 6)]
    df = df.reset_index()

    reset = True
    while reset:

        for index, date in enumerate(dates):

            if date.weekday() not in [0, 1, 2, 3, 4]:

                dates[index:] = [item + datetime.timedelta(days=1) for item in dates[index:]]
                break

            if index >= (len(dates) - 1):
                reset = False

    result = pd.DataFrame(data=zip(dates, prediction),
                        columns=['Date', 'Adj Close'])

    df = df.append(result)
    df = df.reset_index()

    result['Trend'] = pd.Series((1.0 - df['Adj Close'].shift(1) /
        df['Adj Close']) * 100.0)[-5:].reset_index(drop=True)

    return result

