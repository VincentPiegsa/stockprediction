'''
__init__.py -> Sammelt Daten über den Aktienkurs
'''

import datetime
import pandas_datareader.data as web


def get_data(stock):
    """Sammelt Daten über den Aktienkurs
    
    Args:
        stock (str): Aktienname
    
    Returns:
        np.array: Aktienkurs
    """
    start = datetime.datetime(2000, 1, 1)
    end = datetime.datetime.today()

    try:

        df = web.DataReader(stock, 'yahoo', start, end)
         
        return df

    except Exception as e:

        print(e)
        return
