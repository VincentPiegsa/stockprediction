"""
__init__.py -> 
"""
import plotly
import plotly.graph_objs as go
import json


def candlestick(data, name):
    """Stellt die Daten als Candlestick-Graph dar
    
    Args:
        data (TYPE): Daten
        name (str): Name
    
    Returns:
        json: JSON Daten
    """
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'],
                             low=data['Low'], close=data['Close']))

    fig.update_layout(title_text=name)

    fig.update_layout(
        xaxis=go.layout.XAxis(
            title_text='Date',
            rangeselector=dict(
            buttons=list([
                dict(count=5,
                     label="5 Days",
                     step="day",
                     stepmode="backward"),
                dict(count=1,
                     label="1 Month",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6 Months",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="1 Years",
                     step="year",
                     stepmode="backward"),
                dict(count=5,
                     label="5 Years",
                     step="year",
                     stepmode="backward"),
                dict(label="All",
                     step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
        ),
        yaxis=go.layout.YAxis(
            title_text='OHLC'    
        ),
        hovermode='x'
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
